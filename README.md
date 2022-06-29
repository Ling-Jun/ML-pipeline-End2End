# Folder structure

# Github Actions workflow YAML file (NEEDS UPDATE)

```

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
1. If I already have the model in the `deploy` dir on Github repo, then the workflow will fail if I manually trigger it a 2nd time. It gives the error of `nothing to commit, working tree clean`, so this means I need to version the model somehow and update the model version each time I run the workflow. 
2. If I run the workflow a 2nd time after triggering it, it can fail at the `push to Heroku` step, saying that `Updates were rejected because the remote contains work that you do not have locally. This is usually caused by another repository pushing to the same ref.`
