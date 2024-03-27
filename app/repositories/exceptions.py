from fastapi import HTTPException


class RepositoryBaseException(HTTPException):
    default_status_code = 500
    default_detail = "Repository error"

    def __init__(self, status_code: int = None, detail: str = None):
        if not status_code:
            status_code = self.default_status_code
        if not detail:
            detail = self.default_detail
        super().__init__(status_code=status_code, detail=detail)


class RepositoryNotSettedException(RepositoryBaseException):
    def __init__(self):
        detail = "Repository is not setted up. Check config.py"
        super().__init__(status_code=self.default_status_code, detail=detail)


class RepositoryNotFoundException(RepositoryBaseException):
    def __init__(self, name):
        detail = (f"Repository with the name '{name}' was not found. "
                  "Check config.py")
        super().__init__(status_code=self.default_status_code, detail=detail)


class RepositoryConfigException(RepositoryBaseException):
    def __init__(self, name):
        detail = "Repository config error"
        super().__init__(status_code=self.default_status_code, detail=detail)


class AppNotSettedException(RepositoryBaseException):
    def __init__(self):
        detail = "App is not setted up. Check your repository"
        super().__init__(status_code=self.default_status_code, detail=detail)


class AppNotFoundException(RepositoryBaseException):
    def __init__(self, name):
        detail = (f"App with the name '{name}' was not found. "
                  "Check config.py")
        super().__init__(status_code=self.default_status_code, detail=detail)
