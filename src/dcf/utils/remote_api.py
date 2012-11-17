def configure(host=None):
    secure = True
    if not host:
        host = "localhost:8080"
        secure = False
    import google.appengine.ext.remote_api.remote_api_stub as remote_api_stub

    def auth_func():
        # Probably localhost, so let's skip and give some fake admin user
        if host.split(":")[0] in ("localhost", "127.0.0.1"):
            return ("a@b", "b")

        import getpass
        return (raw_input('email: '), getpass.getpass('password: '))

    remote_api_stub.ConfigureRemoteApi(
        None,
        "/_ah/remote_api",
        auth_func,
        host,
        save_cookies=True,
        secure=secure
    )
    remote_api_stub.MaybeInvokeAuthentication()
