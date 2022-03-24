import os
import stat
import certifi


def installCerts():
    """
    Sets the proper perms and location for the ``ssl`` certificate needed to run the bots. This is necessary to run on the first time the app gets started.

    - Sets environment variable ``SSL_CERT_FILE`` to the location of ``certifi``'s premade certificate

    - Sets perms on the file to whatever they need to be for it to be used
    """
    os.environ['SSL_CERT_FILE'] = certifi.where()
    import ssl
    # ssl build (which happens on import) needs to happen after enviro var is set
    STAT_0o775 = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
                  | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
                  | stat.S_IROTH | stat.S_IXOTH)
    # This is pretty complicated. The variable is a collection of bits representing a lot of different perms.
    # As you can tell, it will be given to the certificate once it is set.
    cafile = ssl.get_default_verify_paths().cafile
    # SSL looks for the environment var that was set above when it gives you default verify paths. this is the path to the certificate
    os.chmod(cafile, STAT_0o775)
    # change file permissions so the certificate can be used as intended
    # I don't really understand exactly why this has to be here but it does.
