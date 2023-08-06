import datetime
import pytest
import mock
from copy import deepcopy
import os
import json
import shutil
import tempfile
import time
import botocore.auth
import ssmbotocredentialprovider.FakeMetadata


FAKE_CRED_CONTENTS = """
[default]
aws_access_key_id = fake_access_key
aws_secret_access_key = fake_secret_key
aws_session_token = fake_token
"""

FAKE_REGISTRATION_DATA = '{"ManagedInstanceID":"mi-xyzzy","Region":"us-test-1"}'


class TestFakeMetadata(object):
    def setup(self):
        self.credential_file = tempfile.mktemp()
        self.ssm_registration_file = tempfile.mktemp()
        
        with open(self.credential_file, "w") as f:
            f.write(FAKE_CRED_CONTENTS)

        with open(self.ssm_registration_file, "w") as f:
            f.write(FAKE_REGISTRATION_DATA)
            
        self.cp = ssmbotocredentialprovider.FakeMetadata.FakeMetadataCredentialProvider(credential_file=self.credential_file,
                                                                                        ssm_registration_file=self.ssm_registration_file)
        assert self.cp.credential_file == self.credential_file

    def teardown(self):
        os.unlink(self.credential_file)

    def test_metadata(self):
        metadata = self.cp.metadata
        assert metadata == {
            'account_id': '408421710122',
            'device_name': 'i-12345',
            'region': 'us-test-1',
            'role_alias_name': 'FakeRole'
        }

        
    def test_metadata_credentials(self):
        metadata_creds = self.cp.metadata_credentials

        del metadata_creds["Expiration"]
        del metadata_creds["LastUpdated"]        
        assert metadata_creds == {
            'AccessKeyId': 'fake_access_key',
            'Code': 'Success',
            'SecretAccessKey': 'fake_secret_key',
            'Token': 'fake_token',
            'Type': 'AWS-HMAC'}

    def test_role_name(self):
        assert self.cp.role_name == "FakeRole"

    @mock.patch.object(ssmbotocredentialprovider.FakeMetadata.FakeMetadataCredentialProvider, "get_credentials")
    def test_update_timer(self, mock_get_credentials):
        self.cp.update_timer(refresh_time_seconds=1)
        time.sleep(2)
        assert mock_get_credentials.called is True

    def test_cancel_timer_no_timer(self):
        assert not hasattr(self.cp, "_update_timer")
        self.cp.cancel_timer()
        assert not hasattr(self.cp, "_update_timer")

    @mock.patch.object(ssmbotocredentialprovider.FakeMetadata.FakeMetadataCredentialProvider, "get_credentials")
    def test_cancel_timer(self, mock_get_credentials):
        self.cp.update_timer(refresh_time_seconds=2)
        time.sleep(1)
        self.cp.cancel_timer()
        time.sleep(2)
        assert mock_get_credentials.called is False

    @mock.patch.object(ssmbotocredentialprovider.FakeMetadata.FakeMetadataCredentialProvider, "get_credentials")
    def test_get_refresh_seconds(self, mock_get_credentials):
        retval = {
            'accessKeyId': 'fake_access_key',
            'secretAccessKey': 'fake_secret_key',
            'sessionToken': 'fake_token',
            'expiration': '2020-12-23T17:08:37Z',
        }

        expire_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        retval['expiration'] = expire_time.strftime(botocore.auth.ISO8601)
        mock_get_credentials.return_value = retval

        refresh = self.cp.get_refresh_seconds()
        assert refresh > 0.7*3600
        assert refresh < 3600
