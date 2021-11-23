from typing import Dict, List, Optional, Union, overload


class AbstractDatabase:
    def __raise_abstract_error__(self, msg: Optional[str] = None):
        raise NotImplementedError("Calling a method of AbstractDatabase!" or msg)

    def add_project(self, project_name: str, tags: List[str]):
        self.__raise_abstract_error__()

    def delete_project(self, project_name: str):
        self.__raise_abstract_error__()

    def update_project(self, project_name: str, new_scheme: List[str]):
        self.__raise_abstract_error__()

    def add_model(
        self,
        project_name: str,
        model_name: str,
        model_path: str,
        tag_values: Dict[str, Union[str, int, float]]
    ):
        self.__raise_abstract_error__()

    def delete_model(self, project_name: str, model_name: str):
        self.__raise_abstract_error__()

    def update_model(self, project_name: str, model_name: str, tag_values: Dict[str, Union[str, int, float]]):
        self.__raise_abstract_error__()
