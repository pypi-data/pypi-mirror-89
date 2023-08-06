# -*- coding: utf-8 -*-
import os
import json
import uuid
import logging
from .vulcan2studio import transform_json_from_vulcan_to_studio
from ...thread_base import Greenlet
from ...common import SUPPORTED_IMAGE_INPUT_FORMAT, SUPPORTED_VIDEO_INPUT_FORMAT
from ...json_schema import JSONSchemaType, validate_json
from ...exceptions import DeepoOpenJsonError, DeepoUploadJsonError


BATCH_SIZE = int(os.getenv('DEEPOMATIC_CLI_ADD_IMAGES_BATCH_SIZE', '10'))
LOGGER = logging.getLogger(__name__)


class UploadImageGreenlet(Greenlet):
    def __init__(self, exit_event, input_queue, current_messages,
                 helper, task, on_progress=None, set_metadata_path=False,
                 **kwargs):
        super(UploadImageGreenlet, self).__init__(exit_event, input_queue,
                                                  current_messages=current_messages)
        self.args = kwargs
        self.on_progress = on_progress
        self._helper = helper
        self._task = task
        self._set_metadata_path = set_metadata_path

    def process_msg(self, msg):
        url, batch = msg
        files = {}
        meta = {}
        for file in batch:
            try:
                self.current_messages.report_message()

                # Update file
                files.update({file['key']: open(file['path'], 'rb')})

                # Update corresponding metadata
                file_meta = file.get('meta', {})
                if self._set_metadata_path:
                    if 'data' in file_meta:
                        file_meta['data']['image_path'] = file['path']
                    else:
                        file_meta['data'] = {'image_path': file['path']}
                meta[file['key']] = file_meta
            except RuntimeError as e:
                self.current_messages.report_error()
                LOGGER.error('Something when wrong with {}: {}. Skipping it.'.format(file['path'], e))
        try:
            rq = self._helper.post(url, data={"objects": json.dumps(meta)}, content_type='multipart/mixed', files=files)
            self._task.retrieve(rq['task_id'])
        except RuntimeError as e:
            self.current_messages.report_errors(len(meta))
            LOGGER.error("Failed to upload batch of images {}: {}.".format(files, e))

        for fd in files.values():
            try:
                fd.close()
            except Exception:
                pass

        if self.on_progress:
            self.on_progress(len(batch))
        self.current_messages.report_successes(len(batch))


class DatasetFiles(object):
    def __init__(self, helper, output_queue):
        self._helper = helper
        self.output_queue = output_queue

    def flush_batch(self, url, batch):
        if len(batch) > 0:
            self.output_queue.put((url, batch))
        return []

    def fill_flush_batch(self, url, batch, path, meta=None):
        image_key = uuid.uuid4().hex
        img = {"key": image_key, "path": path}
        if meta is not None:
            meta['location'] = image_key
            img['meta'] = meta
        batch.append(img)
        if len(batch) >= BATCH_SIZE:
            return self.flush_batch(url, batch)
        return batch

    def fill_queue(self, files, project_name):
        total_files = 0
        url = 'v1-beta/datasets/{}/images/batch/'.format(project_name)
        batch = []

        for upload_file in files:
            extension = os.path.splitext(upload_file)[1].lower()
            # If it's an image file add it to the queue
            if extension in SUPPORTED_IMAGE_INPUT_FORMAT:
                meta = {'file_type': 'image'}
                batch = self.fill_flush_batch(url, batch, upload_file, meta=meta)
                total_files += 1

            # If it's a video file add it to the queue
            elif extension in SUPPORTED_VIDEO_INPUT_FORMAT:
                meta = {'file_type': 'video'}
                batch = self.fill_flush_batch(url, batch, upload_file, meta=meta)
                total_files += 1

            # If it's a json, deal with it accordingly
            elif extension == '.json':
                # Verify json validity
                try:
                    with open(upload_file, 'r') as fd:
                        json_data = json.load(fd)
                except IOError as e:
                    raise DeepoOpenJsonError("Upload JSON file {} failed: {}".format(upload_file, e))
                except ValueError:
                    raise DeepoOpenJsonError("Upload JSON file {} is not a valid JSON file".format(upload_file))

                is_valid_json, error, schema_type = validate_json(json_data)
                if is_valid_json:
                    # If it's a Studio json, use it directly
                    if schema_type == JSONSchemaType.STUDIO:
                        studio_json = json_data
                        LOGGER.warning("{} JSON {} validated".format(schema_type, upload_file))
                    # If it's a Vulcan json, transform it to Studio
                    elif schema_type == JSONSchemaType.VULCAN:
                        studio_json = transform_json_from_vulcan_to_studio(json_data)
                        LOGGER.warning("Vulcan JSON {} validated and transformed to Studio format".format(upload_file))
                # If the JSON is not valid but its type is known, print the error
                elif schema_type is not None and error is not None:
                    LOGGER.warning("Error with {} JSON : {} in the instance {}".format(schema_type, error.message, list(error.path)))
                    raise DeepoUploadJsonError("Upload JSON file {} is not a proper {} JSON file".format(upload_file, schema_type))
                # If the schema type is not known, print the error message
                else:
                    raise DeepoUploadJsonError("Upload JSON file {} is neither a proper Studio or Vulcan JSON file".format(upload_file))

                # Add files to the queue
                for ftype in ['images', 'videos']:
                    file_list = studio_json.get(ftype, None)
                    if file_list is not None:
                        for img_json in file_list:
                            img_loc = img_json['location']
                            img_json['file_type'] = ftype[:-1]
                            file_path = os.path.join(os.path.dirname(upload_file), img_loc)
                            if not os.path.isfile(file_path):
                                LOGGER.error("Can't find file named {}".format(img_loc))
                                continue
                            batch = self.fill_flush_batch(url, batch, file_path, meta=img_json)
                            total_files += 1
            else:
                LOGGER.info("File {} not supported. Skipping it.".format(upload_file))
        self.flush_batch(url, batch)
        return total_files

    def post_files(self, org_slug, project_name, files):
        # Retrieve endpoint
        try:
            request = 'orgs/{}/projects/{}/'.format(org_slug, project_name)
            self._helper.get(request)
        except RuntimeError:
            raise RuntimeError("Can't find the project {}".format(project_name))
        return self.fill_queue(files, project_name)
