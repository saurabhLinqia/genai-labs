# Document Q&A using Retrieval Augmented Generation (RAG) and Text Embeddings with a Vector Store

### This lab demonstrates how to implement RAG functionality using Sagemaker Studio, Postgres Pgvector in RDS, and the LLama2 Foundation Model in Sagemaker Jumpstart. We will deploy and configure a RDS instance with Pgvector, then parse, embed, and load a public company's SEC document into the vector store. Lastly, we will prompt the Llama 2 LLM with questions about the document and relevant text chunks from the document retrieved from Pgvector. 


## Prerequisites
- You need a computer with a web browser, preferably with the latest version of Chrome / FireFox.
- Access to an AWS account with sufficient permissions to create and configure RDS instances, Sagemaker Studio and deploy Sagemaker endpoints.

## Recommended background 
It will be easier to complete the workshop if you have: 
- Experience with Deep learning models
- Experience writing Python code in Jupyter notebooks
- Familiarity (100+ level) with Sagemaker Studio and Sagemaker Hosting/Inference

## Target audience
- Data Scientists, ML Engineering, ML Infrastructure, MLOps Engineers, Technical Leaders.
- Intended for customers working with large Generative AI models for text and chat/bot use-cases.
- Level of expertise - 300-400

## Setup
These notebooks and dependent code are intended to be run in Sagemaker Studio but can be run from anywhere with connectivity to AWS with minor modidictions. Adequate permissions to create an RDS instance and associated security group are required. The following lab setup instructions assume you are using a Workshop Studio account with a Sagemaker Studio domain and user already deployed and configured with adequate permissions. 

### Step 1: Clone the repo into Sagemaker Studio
Open Sagemaker Studio, click on the Git icon on the left nav, then click the `Clone a repository` button. Paste the lab's github url and push `Clone`. Sagemaker Studio will open a terminal window and git clone the repo into your environment. Repo url: `https://github.com/matgillen/genai-labs.git`

### Step 2: Use Sagemaker Jumpstart to deploy the Llama 2 7b chat model to an endpoint
In Sagemaker Studio on the Studio `Home` page, click the JumpStart link to open Sagemaker Jumpstart. In the search bar at the top of the window, search for `llama` and find the model named `llama-2-7b-chat`. Click the `View model` button to open the model page. Look for the `Deployment configuration` section and expand it. Change the `Sagemaker hosting instance` value to `ml.g5.4xlarge` and then click the `Deploy` button at the bottom of the section. Accept the model EULA to deploy the model. This usually takes 5-10 minutes.

### Step 3: Use Sagemaker Jumpstart to deploy the Text Embedding model
Go back to the Jumpstart main page and search for `Text Embedding` and find the model named `All MiniLM L6 v2`. Click the `View model` button to open the model page, then click "Deploy" to deploy this model using the default configuration and settings. This usually takes 1-2 minutes

### Step 4: Deploy and configure the RDS instance
Click the file folder icon on the left nav in Sagemaker Studio. Navigate into the lab repo to ```[home folder]/genai-labs/rag_pgvector``` and open the notebook ```1_deploy_rds_postegres.ipynb```. In order to run the code, we'll need to start the Kernel instance by pressing the `Select` button when the Kernal launcher dialog pops up. First, make sure the image is `Data Science 3.0` and Kernel is `Python 3`. The default instance type is sufficient.

While the notebook kernel is starting, go back to the studio lab home page and copy the AWS IAM keys and session token. Then paste them into the first code cell in the notebook. If they are prefixed with the `export` command, remove that from each line so we are left with 3 variable assignment statements. 

Once the notebook kernel starts, execute the notebook to create the RDS instance by running each cell in the notebook through cell 11 labeled `Check deployment status`. The instance will take 5-10 minutes to finish the deployment cycle. In the meantime, we'll take a look at the presentation and learn about Retrieval Augmented Generation with Text Embeddings.  





