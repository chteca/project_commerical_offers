### Overview

This project is designed to generate commercial proposals in response to client requests. The trained Random Forest Regressor model predicts the marginality of a product based on the input data, and the application generates a commercial proposal based on the input data and marginality. The project also utilizes the Tesseract OCR model for catalog number recognition in images.

This application predicts product margins based on historical sales data and generates a commercial offer in a few seconds, which significantly saves a sales specialist’s time.

### Structure
The repository is organized into several components:

- **Folder**: `cp`
  - **Files**:
    - `file1.xls`: example of a commercial proposal generated by the application
    - `sample.xlsx`: sample for a commercial proposal

- **Folder**: `data`
  - **Files**:
    - `clients.csv`: dataset with customer information
	- `cp3.csv`: dataset with the history of commercial offers on which the model was trained
	- `clients.csv`: dataset with product information
	
- **Folder**: `images`
  - **Files**:
    - `лот4_5.png`: example image with client request
	
- **Folder**: `models`
  - **Files**:
    - `best_model_rfr.sav`: trained model for predicting margins
	- `encoding_model.sav`: trained model to encode input data

- **Files**: `
	- `create_xls_file.py`: script to generate xlx file
	- `prediction_endpoint.py`: script to get a prediction
	- `preprocess.py`: script to preprocess input data
	- `requirements.txt`
	- `schemas.py`: pydantic models
	- `tesseract.py`: script to search catalog number in images
	- `utils.py`: 
	
## How to use
1. **In a terminal, navigate to the directory where you want to copy the repository and run the command**

    ```bash
    git clone https://github.com/chteca/project_commerical_offers
    ```

2. **Install the required libraries**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the FastAPI application**

    ```bash
   uvicorn prediction_endpoint:app 
    ```

4. **Sent the input data**
Below is an example of the input data.

    ```bash
   http -v POST http://localhost:8000/prediction client="Санта Бремор" procurement="закупка" delivery_time=60 catalog_number="SPR00SIA1, TANKMPK03" quantity=1 contract=1 merck_competitors=0 other_competitors=0 
    ```
  Instead of specifying catalog numbers, you can use the path to the image where they are listed.

  ```shell
  http -v POST http://localhost:8000/prediction client="Ганцевичи СПК" procurement="тендер" delivery_time=60 path_file="./images/лот4_5.png" quantity=1 contract=1 merck_competitors=0 other_competitors=1
  ```








### Results
After executing all commands the products' margin will appear in the terminal, and a file **'file1.xls'** with the finalized commercial offer will be created in the folder **./cp**.

![Image alt](https://github.com/chteca/project_commerical_offers/raw/master/images/request_example1.png)

![Image alt](https://github.com/chteca/project_commerical_offers/raw/master/images/cp_example1.png)

![Image alt](https://github.com/chteca/project_commerical_offers/raw/master/images/request_example2.png)

![Image alt](https://github.com/chteca/project_commerical_offers/raw/master/images/cp_example2.png)
