from . import errors
from . import config
from . import types
from . import util


def get_version(
    root_version=config.DEFAULT_ROOT_VERSION,
    read_revision_info=config.DEAULT_READ_REVISION_INFO,
    parse_tag=config.DEFAULT_PARSE_TAG,
    create_version=config.DEFAULT_CREATE_VERSION,
):
    revision_info = read_revision_info()

    if revision_info is None:
        version_from_pkg_info_file = get_version_from_pkg_info_file()
        if version_from_pkg_info_file is None:
            raise errors.RevisionInfoNotFoundError('No revision info available.')

        return version_from_pkg_info_file

    if revision_info.latest_tag is None:
        latest_release_version = root_version

    else:
        latest_release_version = parse_tag(revision_info.latest_tag)

    version_data = types.VersionInfo(
        latest_release=latest_release_version,
        distance=revision_info.distance,
        commit=revision_info.commit,
        dirty=revision_info.dirty,
    )

    return create_version(version_data)


def get_version_from_pkg_info_file():
    try:
        return util.parse_pkg_info_file('PKG-INFO')['Version']

    except (PermissionError, FileNotFoundError):
        return None
