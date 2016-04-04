import hashlib
import os.path
import shutil


class SerializationDatabase(object):
    def __init__(self, path):
        """
        @param path A directory to copy and store all files serialized
        through this database
        """
        self.path = path

    def get_key(self, source_path, extension=None):
        """
        Generate a key composed from the hash of the 
        data in source_path and the given extension 
        @param source_path A file to hash
        @param extension The extension for the key (if None, the
        extension on the source_path file is used)
        @return A unique key for the source_path
        """
        if extension is None:
            _, extension = os.path.splitext(source_path)
        return self._get_hash(source_path) + extension

    def get_path(self, key, verify=True):
        """
        @param key The key (generated by get_key)
        @param verify TODO
        """
        if len(key) == 0:
            raise IOError('Empty key.')

        resource_path = os.path.join(self.path, key)

        if verify:
            key_hash, _ = os.path.splitext(key)
            resource_hash = self._get_hash(resource_path)

            if resource_hash != key_hash:
                raise IOError(
                    'Hash mismatch "{:s}" has hash {:s}; expected {:s}.'
                    .format(resource_path, resource_hash, key_hash))

        return resource_path

    def save(self, source_path, extension=None):
        """
        Compute a key from the hash of the source_path file.
        Then copy the source_path file into the database's directory
        and return the key
        @param source_path The file to be hashed and saved
        @param extension The extension to use when saving the file
        @return The key computed from the hash
        """
        key = self.get_key(source_path, extension)
        shutil.copyfile(source_path, self.get_path(key, verify=False))
        return key

    def _get_hash(self, source_path):
        """
        Generate a hash of the original source file
        @param source_path The source file to generate hash of
        @return The hash
        """
        if not os.path.exists(source_path):
            raise IOError(
                'Source path "{:s}" does not exist.'.
                format(source_path))

        with open(source_path, 'rb') as source_file:
            source_content = source_file.read()

        return hashlib.md5(source_content).hexdigest()

# def serialize_kinbody(kinbody, database):
#     filenames = robot.GetURI()
#     if not filenames:
#         raise ValueError(
#             'Unable to serialize KinBody with empty GetXMLFileName().')

#     return {
#         'XMLId': kinbody.GetXMLId(),
#         'URI': [database.save(path) for path in filenames.split()],
#         'KinematicsGeometryHash': kinbody.GetKinematicsGeometryHash(),
#         'RobotStructureHash': kinbody.GetRobotStructureHash(),
#     }


#     for 

