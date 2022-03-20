import os
import stat
import certifi


def installCerts():
    os.environ['SSL_CERT_FILE'] = certifi.where()
    import ssl
    # ssl build needs to happen after enviro var is set
    STAT_0o775 = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
                  | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
                  | stat.S_IROTH | stat.S_IXOTH)
    cafile = ssl.get_default_verify_paths().cafile
    # change working directory to the default SSL directory
    # os.chdir(cafile_dir)  # Error happens here
    # relpath_to_certifi_cafile = os.path.relpath(certifi.where())
    # print(" -- removing any existing file or link")
    # try:
    #     os.remove(cafile)
    # except FileNotFoundError:
    #     pass
    # print(" -- creating symlink to certifi certificate bundle")
    # os.symlink(relpath_to_certifi_cafile, openssl_cafile)
    print(" -- setting permissions")
    os.chmod(cafile, STAT_0o775)
    print(" -- update complete")
