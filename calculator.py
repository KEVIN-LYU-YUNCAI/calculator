import json
import boto3
from datetime import datetime

# 初始化DynamoDB客户端
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CalculationsTable')

def lambda_handler(event, context):
    # 从事件中获取数据
    num1 = event.get('num1')
    num2 = event.get('num2')
    operation = event.get('operation')
    result = event.get('result')
    user_id = event.get('userId')
    
    # 生成唯一的ID
    calculation_id = f"{user_id}_{str(int(datetime.now().timestamp()))}"
    
    # 当前时间戳
    timestamp = int(datetime.now().timestamp())
    
    # 构建DynamoDB的PutItem请求
    item = {
        'id': calculation_id,
        'userId': user_id,
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'result': result,
        'timestamp': timestamp
    }
    
    # 将数据写入DynamoDB
    try:
        response = table.put_item(Item=item)
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps('Calculation stored successfully')
        }
    except Exception as e:
        # 错误处理
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error storing calculation: {str(e)}")
        }
