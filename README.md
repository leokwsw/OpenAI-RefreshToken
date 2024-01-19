# Use PandoraNext looping to get ChatGPT AccessToken

- Welcome to Create PR to fix bugs and Create issues to tell me more about anythings
- The License is MIT

1. clone project
   ```bash
   git clone https://github.com/leokwsw/PandoraNext-RefreshToken
   cd PandoraNext-RefreshToken
   ```
2. get PandoraNext License [Link](https://docs.pandoranext.com/zh-CN/license/license_id)
3. copy PandoraNext config and token file, and
   follow [config.json](https://docs.pandoranext.com/zh-CN/configuration/config)
   and [tokens.json](https://docs.pandoranext.com/zh-CN/configuration/tokens) to set up PandoraNext
   ```bash
   cd pandoranext/data
   cp example.config.json config.json
   # edit config.json
   cp example.tokens.json tokens.json
   # edit tokens.json
   cd ../
   docker-compose up -d
   ```
4. copy and edit config file
   ```bash
   cd ../
   cp config_template.yaml config.yaml 
   # edit config file
   ```
5. copy and edit account.json
   ```bash
   cp example.account.json account.json 
   # edit account file
   ```
   Please follow the json format below
   ```json lines
   [
     {
       "email": "openai1@example.com",
       "password": "password"
     },
     {
       "email": "openai2@example.com",
       "password": "password"
     },
     ...
   ]
   ```

6. install dependency
   ```bash
   pip install -r requirements.txt
   ```

7. run it
   ```bash
   python main.py
   ```

8. after the python finish to run, the json file named `account.json` will be look like this
   ```json lines
   [
     {
       "email": "openai1@example.com",
       "password": "password",
       "access_token": "{{JWT Token}}",
       "access_token_expire_at": "2024-01-29 10:14:19.929272"
     },
     {
       "email": "openai2@example.com",
       "password": "password",
       "access_token": "{{JWT Token}}",
       "access_token_expire_at": "2024-01-29 10:15:00.479372"
     },
     ...
   ]
   ```

9. you can use the `access_token` to call ChatGPT API.