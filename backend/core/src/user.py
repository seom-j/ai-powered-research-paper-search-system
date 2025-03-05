from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from utils import googleOAuth, MySQLHandler
import requests

# ********************************************* #
# ***************  About  User  *************** #
# ********************************************* #

async def create_new_user(data):
    """새로운 사용자 생성 로직"""
    pass

async def login_user(data):
    print("===  /login ===")
    oauth = googleOAuth()
    return RedirectResponse(
        f"{oauth.authorization_url}?response_type=code&client_id={oauth.client_id}&redirect_uri={oauth.redirect_uri}&scope=openid%20email%20profile"
    )

async def oauth_callback(data):
    print("=== GET /auth/callback ===")
    try :
        code = data.get("code")
        print("code : ", code)
    except Exception as e:
        print(f"Missing key in parameters: {e}")
        raise HTTPException(status_code=400, detail="Invalid parameters")

    try :
        oauth = googleOAuth()
        token_response = requests.post(
            oauth.token_url,
            data={
                "code": code,
                "client_id": oauth.client_id,
                "client_secret": oauth.client_secret,
                "redirect_uri": oauth.redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        token_response_data = token_response.json()

        access_token = token_response_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Invalid token")

        user_info_response = requests.get(
            oauth.user_info_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = user_info_response.json()

        name = user_info.get("name", "")
        email = user_info.get("email", "")

    except Exception as e:
        print(f"Error in OAuth callback: {e}")
        raise HTTPException(status_code=500, detail="OAuth callback error")
        
    try :
        db_handler = MySQLHandler()
        db_handler.connect()
        insert_query = "INSERT INTO DOCUMENTO.user_tb (email, name) VALUES (%s, %s)"
        db_handler.execute_query(insert_query, (email, name))
        print(f"Inserted email: {email}, name: {name} into DOCUMENTO.user_tb")
    except Exception as e:
        print(f"Error with insert to MySQL: {e}")
    finally:
        db_handler.disconnect()
    
    output_data = {}
    return JSONResponse(content=output_data, status_code=200)

async def logout_user(data):
    """사용자 로그아웃 처리 로직"""
    pass

async def reissue_user_token(data):
    """사용자 토큰 재발급 로직"""
    pass


