from flask_restful_swagger_2 import Api, swagger, Resource


class Parameter_in:
    path="path"
    query="query"
    header="header"
    body="body"
    formData="formData"


class SwaggerParameter:
    def __new__(cls,name,description,args_in,required=True,data_type=None,schema=None):
        """
        each api needs parameters then init it
        if data type is not body
        then dont need schema
        :param name:string
        :param description:string
        :param args_in: Parameter_in(string)
        :param data_type: string, it means like interger,string ...
        :param required: bool
        :param schema: Schema of Swagger
        :return:
        """
        mydict={
            "name":name,
            "description":description,
            "in":args_in,
            "required":required,
            "schema":schema,
            "type":data_type,
        }
        if args_in!="body":
            mydict["type"]=data_type
        return mydict

class SwaggerResponse:
    def __new__(cls,code,description,schema,examples=None,headers=None):
        """

        :param code:int ex:200,900
        :param description: string
        :param schema: schema of Swagger
        :param examples: dict of examples
        :param headers: dict of headers
        :return:
        """
        mydict={
            str(code):{
                'description': description,
                'schema': schema,
                "headers":headers,
                "examples":examples,
            }
        }

        return mydict



class SwaggerDoc:
    def __new__(cls, tags,description,parameters,responses,deprecated=False):
        """
        @swagger.doc need this init
        :param tags: array
        :param description: string
        :param parameters:array of SwaggerParameter
        :param responses: dict, maybe it is multiple like 200 404...etc
        :return:
        """
        return {
            "tags":tags,
            "description":description,
            "parameters":parameters,
            "responses":responses,
            "deprecated":deprecated,

        }