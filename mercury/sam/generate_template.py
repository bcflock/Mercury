
import re 
from typing import List, Tuple


def make_yaml_start_str(**kwargs) -> str: 
    return """

AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  DashboardDataAPISAM{env}

  Sample SAM{env} Template for DashboardDataAPISAM{env} || DashboardDataAPISAM{env}

# More info about Globals: https://github.com/awslabs/serverless-application-model/blob/master/docs/globals.rst
Globals:
  Function:
    Timeout: 30
    MemorySize: 128

Resources:

  # ---------------------- rest api ------------------------------------------------------------------------------------------

  DashboardDataAPIGatewaySAM{env}:
    Type: AWS::Serverless::Api
    Properties:
      StageName: {env}
      Cors: "'*'"
      Auth:
        DefaultAuthorizer: DashboardCognitoAuthorizer
        Authorizers:
          DashboardCognitoAuthorizer:
            UserPoolArn: !GetAtt DashboardCognitoUserPoolSAM{env}.Arn
            AuthorizationScopes:
              - aws.cognito.signin.user.admin
            IdentitySource: "$request.querystring.param"

  # ---------------------- auth with cognito setup ------------------------------------------------------------------------------------------

  DashboardCognitoUserPoolSAM{env}:
    Type: AWS::Cognito::UserPool
    Properties:
      UserPoolName: DashboardCognitoUserPoolSAM{env}
      Policies:
        PasswordPolicy:
          MinimumLength: 8
      UsernameAttributes:
        - email
      Schema:
        - AttributeDataType: String
          Name: email
          Required: false
  
  DashboardCognitoUserPoolClientSAM{env}:
    Type: AWS::Cognito::UserPoolClient
    Properties:
      UserPoolId: !Ref DashboardCognitoUserPoolSAM{env}
      ClientName: DashboardCognitoUserPoolClientSAM{env}
      GenerateSecret: false




    """.format(**kwargs)


def make_function_str(**kwargs) -> str:
    return """

  DashboardDataAPISAM{env}{func_name}:
    Type: AWS::Serverless::Function # More info about Function Resource: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Properties:
      FunctionName: DashboardDataAPISAM{env}{func_name}
      CodeUri: {code_path}
      Handler: app.lambda_handler
      Runtime: python3.9
      Architectures:
       - x86_64
      Policies:
        - Statement:
          - Effect: Allow
            Action: 
              - secretsmanager:GetResourcePolicy
              - secretsmanager:GetSecretValue
              - secretsmanager:DescribeSecret
              - secretsmanager:ListSecretVersionIds
            Resource: 
              - "arn:aws:secretsmanager:us-east-1:642434499290:secret:rds!db-0618ae26-69a7-42ba-8476-f7ed63eaff5f-eetSyz"
        - Statement:
          - Effect: Allow
            Action:
              - lambda:InvokeAsync
              - lambda:InvokeFunction
            Resource: 
              - "arn:aws:lambda:us-east-1:642434499290:function:rds-postgre-sql-executor"
        - Statement: 
          - Effect: Allow
            Action:
              - s3:Get*
              - s3:List*
              - s3:Describe*
              - s3-object-lambda:Get*
              - s3-object-lambda:List*
            Resource: "*"
      Events:
        {func_name}Route:
          Type: Api
          Properties:
            RestApiId: !Ref DashboardDataAPIGatewaySAM{env}
            Path: {http_path}
            Method: {http_method}

    """.format(**kwargs)



def make_yaml_return_str(**kwargs) -> str: 
    return """

Outputs:
  # ServerlessRestApi is an implicit API created out of Events key under Serverless::Function
  # Find out more about other implicit resources you can reference within SAM{env}
  # https://github.com/awslabs/serverless-application-model/blob/master/docs/internals/generated_resources.rst#api
  DashboardCognitoUserPoolClientSAM{env}:
    Description: "This is the DashboardCognitoUserPoolClientSAM{env}"
    Value: !Ref DashboardCognitoUserPoolClientSAM{env}

    """.format(**kwargs)

http_method_map = {
    "GetA": "GET", 
    "GetAn": "GET",
    "GetAll": "GET", 
    "GetSome": "GET", 
    "Create": "PUT", 
    "Modify": "PATCH", 
    "Delete": "DELETE", 
    "Upload": "PUT" 
}


def get_http_method_of_name(func_name, check_methods=["GetAll", "GetAn", "GetA", "Create", "Delete", "Modify", "Upload"]):  
  # must check GetAll before GetAn and before GetA
  print("function_name:  ", func_name)
  for method in check_methods:
     if func_name[0:len(method)] == method:
      return http_method_map[method]
  print("\nERROR:  Unsupported Method from: ", func_name)
  raise(Exception)


def make_table_id(func_name, check_methods=["GetAll", "GetAn", "GetA", "Create", "Delete", "Modify", "Upload"]):  
  # must check GetAll before GetAn and before GetA
  return make_table_name(func_name=func_name, check_methods=check_methods)+"_id"



def make_table_name(func_name, check_methods=["GetAll", "GetAn", "GetA", "Create", "Delete", "Modify", "Upload"]):  
  # must check GetAll before GetAn and before GetA
  for method in check_methods:
     if func_name[0:len(method)] == method:
      return func_name[len(method):]
  print("\nERROR:  Unsupported Method from: ", func_name)
  raise(Exception)




http_path_map = {
   "GetAll": (lambda table_name, _: "/" + table_name),
   "GetAn": (lambda table_name, table_id: "/" + table_name + "/{" + table_id + "}" ),
   "GetA": (lambda table_name, table_id: "/" + table_name + "/{" + table_id + "}" ),
   "Create": (lambda table_name, _: "/" + table_name),
   "Modify": (lambda table_name, table_id: "/" + table_name + "/{" + table_id + "}" ),
   "Delete": (lambda table_name, table_id: "/" + table_name + "/{" + table_id + "}"),
   "Upload": (lambda table_name, table_id: "/" + table_name + "/{" + table_id + "}/upload" ),
}
def get_http_path_of_name(func_name, table_id="", check_methods=["GetAll", "GetAn", "GetA", "Create", "Delete", "Modify", "Upload"]) -> str:  
  # must check GetAll before GetAn and before GetA
  if table_id == "":
     table_id = make_table_id(func_name)
     table_name = make_table_name(func_name)
  for method in check_methods:
     if func_name[0:len(method)] == method:
      return str.lower(http_path_map[method](table_name, table_id))
  print("\nERROR:  Unsupported Method from: ", func_name)
  raise(Exception)


def make_functions_group(actions: List[str],
                       tablename: str,
                       code_base_path:str, 
                       http_base_path:str, 
                       table_id:str="",
                       env:str="Prod",
                       extra_funcs:List[Tuple[str,str]]=[]) -> str:

  
  functions=[]

  for i in range(len(actions)):

    functions.append(make_function_str(**{
        "env": env, 
        "func_name": actions[i]+tablename, 
        "code_path": code_base_path + "/" + actions[i]+tablename + '_DashboardDataAPI',
        "http_path": http_base_path + get_http_path_of_name(func_name=actions[i]+tablename, table_id=table_id),
        "http_method": get_http_method_of_name(func_name=actions[i]+tablename)
    }))
  for i in range(len(extra_funcs)):

    functions.append(make_function_str(**{
        "env": env, 
        "func_name": extra_funcs[i][0], 
        "code_path": code_base_path + "/" + extra_funcs[i][0] + '_DashboardDataAPI',
        "http_path": extra_funcs[i][1],
        "http_method": get_http_method_of_name(extra_funcs[i][0])
    }))
    
  return "\n\n".join(functions)




# def make_lambda_bundle(actions, http_base_path, code_base_path, tablename, 
#                        table_key_name="", env="Prod", path_override={}, tablename_plural=True):
#     if table_key_name == "":
#         table_key_name = str.lower(tablename) + "_id"
#     function_ls = []
#     for action in actions:
#         if action == "GetA" or action == "Modify" or action == "Delete" or action == "Upload":
#             http_path = http_base_path + "/{" + table_key_name + "}"
#         else:
#             http_path = http_base_path
#         if action.__contains__("Of"):
#             split=action.split("Of")
#             _action = split[0]
#             if tablename_plural: 
#                 _tablename = tablename+"sOf"+split[1]
#             else:
#                 _tablename = tablename+"Of"+split[1]
#             http_path = path_override.get(action, http_path)
#         else:
#             _action = action
#             _tablename = tablename
#         function_ls.append(make_function_str(**{
#             "env": env, 
#             "func_name": func_name,
#             "code_path": code_base_path + _action + _tablename + '_DashboardDataAPI',
#             "http_path": http_path,
#             "http_method": http_method_map[_action]
#         }))
#     return function_ls



