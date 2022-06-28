# Folder structure

# github actions workflow YAML file

```
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: run train script
        env:
          NEPTUNE_API_TOKEN: ${{ secrets.NEPTUNE_API_TOKEN }}
        run: bash ../../ML-pipeline-End2End/ML-pipeline-End2End/train/train.sh
      - name: fetch model from Neptune
        env:
          NEPTUNE_API_TOKEN: ${{ secrets.NEPTUNE_API_TOKEN }}
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
          HEROKU_APP_NAME: ${{ secrets.HEROKU_APP_NAME }}
        run: |
          pip install -r requirements/requirements.txt
          python ./artifacts/models/fetch_model.py
          pwd
          git status
      - name: Commit & push changes
        run: |
          git config --global user.name ${{ secrets.USER_NAME }}
          git config --global user.email ${{ secrets.USER_EMAIL }}
          git add -A
          git commit -m "added model files"
          git push
        # git subtree split --prefix deploy -b deploy
        # git push --force https://heroku:$HEROKU_API_KEY@git.heroku.com/$HEROKU_APP_NAME.git deploy
      - name: deploy to Heroku
        env:
          NEPTUNE_API_TOKEN: ${{ secrets.NEPTUNE_API_TOKEN }}
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
          HEROKU_APP_NAME: ${{ secrets.HEROKU_APP_NAME }}
        run: |
          git subtree push --prefix deploy https://heroku:$HEROKU_API_KEY@git.heroku.com/$HEROKU_APP_NAME.git master
```
- Step: run train script.
> this step uses the repo secret NEPTUNE_API_TOKEN to connect to NEPTUNE to upload the trained model to Neptune. The trainning happens within the Github Actions temporary server that was spun up when we trigger the workflow. 
- Step: fetch model from Neptune
> this step fetches the model from Neptune to the local directory (within the temporary server created by Github Actions), therefore you won't actually see the model file in our repo's corresponding directory.
- Step: Commit & push changes
> This step allows us to tell the temporary server (spun up by Github Actions) to establish a connection with the current repo and push the temp server's version of code (which of course contains the pickled model file that we downloaded from Neptune) to the current repo. 

> After this step is finished, we should be able to see the model file is added in our github repo. This step essentially allows us to modify the current repo with Github Actions. 
- Step: deploy to Heroku
> Use of `git subtree push` command allows us to push a sub dir of the current repo to Heroku for deployment. However, `subtree` cmd doesn't have a `--force` push option, so every time we update the model, we might have trouble push it to Heroku. But that's another topic for another time. 

# Things to improve