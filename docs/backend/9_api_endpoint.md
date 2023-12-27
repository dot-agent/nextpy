
# API Endpoints
   
Nextpyseamlessly integrates a FastAPI backend to power your frontend app. This backend offers the flexibility to create custom API endpoints for diverse purposes, extending your app's capabilities beyond its core functionality.  
   
## Creating Custom API Endpoints:  
   
### 1. Define Your Endpoint Function:  
- Use FastAPI's syntax to define a function that handles incoming requests and returns a JSON response.  
- Example:  
  ```python  
  async def api_test(item_id: int):  
      return {"my_result": item_id}  
  ```  
   
### 2. Register the Endpoint:  
- Use `app.api.add_api_route` to register your function as an API endpoint.  
- Specify the desired path:  
  ```python  
  app = xt.App()  
  app.api.add_api_route("/items/{item_id}", api_test)  
  ```  
   
## Accessing Your Endpoint:  
   
- After compilation, access your custom endpoint via a web browser or tools like Postman, using the specified path and any required parameters.  
- Example: `http://localhost:8000/items/23`  
   
## Reserved Routes:  
   
- Nextpy reserves certain routes for its internal operations:  
  - **Ping:** `/ping/` for checking backend health (expected response: "pong")  
  - **Event:** `/_event` for frontend-backend event communication  
  - **Upload:** `/_upload` for file uploads using `xt.upload()`  
   
---  
   
# Let's Create a First Functional API Endpoint  
   
## 1. Define the Endpoint Function:  
   
- Employ Python's `async def` syntax to create an asynchronous function for efficient request handling:  
  ```python  
  async def calculate_area(length: float, width: float):  
      # Perform the calculation  
      area = length * width  
  
      # Return the result as a JSON response  
      return {"area": area}  
  ```  
   
## 2. Register the Endpoint:  
   
- Use `app.api.add_api_route` to register the function as an API endpoint:  
  ```python  
  app.api.add_api_route("/calculate-area", calculate_area, methods=["POST"])  # Specify POST for calculation submission  
  ```  
   
## 3. Run the app
   
- Type `nextpy run` in terminal to start the app  

## 4. Access the Interactive API Documentation
- Once your app is running, open a web browser and navigate to http://localhost:8000/docs.
- This will take you to the interactive API documentation provided by Swagger UI.
   
## Enhancement Tips:  
   
- **Input Validation:** Ensure valid numerical values for length and width.  
- **HTTP Methods:** Explore using GET for simple retrieval operations.  
- **Expanded Functionality:** Consider adding more complex calculations or data processing capabilities.  
   