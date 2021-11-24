from typing import Dict, List, Optional, Union


def __raise_abstract_error__(msg: Optional[str] = None):
    raise NotImplementedError("Calling a method of AbstractDatabase!" or msg)


class AbstractDatabase:
    def get_project_signature(self, project_name: str):
        __raise_abstract_error__()

    def get_project_models_list(self, project_name: str):
        __raise_abstract_error__()

    def add_project(self, project_name: str, tags: List[str]):
        __raise_abstract_error__()

    def delete_project(self, project_name: str):
        __raise_abstract_error__()

    def update_project(
        self,
        project_name: str,
        names_to_add: List[str],
        names_to_drop: List[str],
        names_to_rename: Dict[str, str]
    ):
        __raise_abstract_error__()

    def add_model(
        self,
        project_name: str,
        model_name: str,
        model_path: str,
        tag_values: Dict[str, Union[str, int, float]]
    ):
        __raise_abstract_error__()

    def delete_model(self, project_name: str, model_name: str):
        __raise_abstract_error__()

    def update_model(
        self,
        project_name: str,
        model_name: str,
        names_to_add: List[str],
        names_to_drop: List[str],
        names_to_rename: Dict[str, str]
    ):
        __raise_abstract_error__()
