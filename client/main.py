import hashlib
import json
import boto3
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import SYS_PROGRAM_ID
from solana.publickey import PublicKey
from solana.transaction.instructions import Instruction
from solana.rpc.commitment import Confirmed
from botocore.exceptions import NoCredentialsError

# 해시생성
def create_hash(video_date, device, location, user):
    data = {
        "video_date": video_date,
        "device": device,
        "location": location,
        "user": user
    }
    json_data = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(json_data).hexdigest()

# Solana 클라이언트 설정
client = Client("https://api.devnet.solana.com")
payer = Keypair.from_secret_key(b"YourSecretKeyHere")

# 비디오 정보 저장 함수

def store_video_info(video_date, device, location, user, hash):
    program_id = PublicKey("YourProgramIdHere")
    video_info_account = Keypair()
    space = 8 + 32 + 32 + 32 + 32 + 64  # Account space for VideoInfo
    lamports = client.get_minimum_balance_for_rent_exemption(space)["result"]

    transaction = Transaction()

    # Create the account instruction
    create_account_instruction = anchor.web3.SystemProgram.createAccount({
        "from_pubkey": payer.public_key,
        "new_account_pubkey": video_info_account.public_key,
        "lamports": lamports,
        "space": space,
        "program_id": program_id,
    })
    transaction.add(create_account_instruction)

    data = {
        "video_date": video_date,
        "device": device,
        "location": location,
        "user": user,
        "hash": hash
    }
    data_bytes = json.dumps(data).encode()

    instruction = Instruction(
        keys=[
            {"pubkey": video_info_account.public_key(), "is_signer": True, "is_writable": True},
            {"pubkey": payer.public_key(), "is_signer": True, "is_writable": False}
        ],
        program_id=program_id,
        data=data_bytes
    )

    transaction.add(instruction)

    result = client.send_transaction(transaction, payer, video_info_account, opts=Confirmed)
    return result

# AWS S3 설정
s3 = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')
bucket_name = 'YOUR_BUCKET_NAME'

def upload_to_s3(file_name, file_path):
    try:
        s3.upload_file(file_path, bucket_name, file_name)
        return f'https://{bucket_name}.s3.amazonaws.com/{file_name}'
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None

# 메인 실행 예시
if __name__ == "__main__":
    video_date = "2023-06-01"
    device = "Camera123"
    location = "Seoul"
    user = "user123"
    hash = create_hash(video_date, device, location, user)

    file_path = 'path/to/your/video.mp4'
    file_name = file_path.split('/')[-1]
    s3_url = upload_to_s3(file_name, file_path)

    if s3_url:
        print(f'Uploaded to S3: {s3_url}')
        result = store_video_info(video_date, device, location, user, hash)
        print(f'Stored on blockchain: {result}')
    else:
        print('Failed to upload video')
