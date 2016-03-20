<?php

require_once("rest.php");

const DB_SERVER = "localhost";
const DB_USER = "u627812499_admin";
const DB_PASSWORD = "password";
const DB = "u627812499_db";

    
class API extends REST 
{
	public $data = "";
	public function __construct()
	{
		parent::__construct();// Init parent contructor
	}

	//Public method for access api.
	//This method dynmically call the method based on the query string
	public function processApi()
	{
		$func = strtolower(trim(str_replace("/"," ",$_REQUEST['request'])));
		if((int)method_exists($this,$func) > 0)
		{
			if (
				$func == "register" ||
				$func == "set_config" ||
				$func == "set_command" ||
                $func == "refresh_config")
			{
				// Cross validation if the request method is POST else it will return "Not Acceptable" status
				if($this->get_request_method() != "POST")
				{
					$error = array('status' => "failed", "msg" => "Use POST request");
					$this->response($this->json($error), 406);
					return;
				}
			}
			if ($func == "get_config" ||
				$func == "getSystemStatus" )
			{
				// Cross validation if the request method is GET else it will return "Not Acceptable" status
				if($this->get_request_method() != "GET")
				{
					$error = array('status' => "failed", "msg" => "Use GET request");
					$this->response($this->json($error), 406);
					return;
				}
			}
			
			$this->$func();
		}
		else
			$this->response('',404); 
		// If the method not exist with in this class, response would be "Page not found".

	}
    
	private function register()
	{		
		$email = $this->_request['email'];
        $system_id = $this->_request['system_id'];
        
        if(empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL))
        {
            $error = array('status' => "failed", "msg" => "Invalid email id");
            $this->response($this->json($error), 406);
            return;
        }
        
        if(empty($system_id) || !$this->valid_guid($system_id))
        {
            $error = array('status' => "failed", "msg" => "Invalid system id");
            $this->response($this->json($error), 406);
            return;
        }
        
        $conn = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB);
        if ($conn->connect_error) {
            $error = array('status' => "failed", "msg" => "Error opening database");
            $this->response($this->json($error), 500);
            return;
        }
        
        $result = $conn->query("SELECT * FROM ACCOUNT WHERE EMAIL='$email'");
        if ($result->num_rows <= 0)
        {
            if ($conn->query("INSERT INTO ACCOUNT (EMAIL, SYSTEM_ID) VALUES ('$email', '$system_id')") === TRUE)
            {
                $success = array('status' => "success", "msg" => "Account registered successfully");
                $this->response($this->json($success), 200);
            }
            else
            {
                $error = array('status' => "failed", "msg" => "Error registering new account");
                $this->response($this->json($error), 400);
            }
        }
        else
        {
            $error = array('status' => "failed", "msg" => "Email address already exists");
            $this->response($this->json($error), 406);                    
        }
        
        $result->close();
        $conn->close();
	}
	
	private function get_config()
	{
        if(!isset($_REQUEST['system_id'])){
            $error = array('status' => "failed", "msg" => "System ID missing in API");
            $this->response($this->json($error), 406);        
        }
        
		$system_id= $this->_request['system_id'];
		
		if(!empty($system_id))
		{
			$conn = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB);
			// Check connection
			if ($conn->connect_error) {
                $error = array('status' => "failed", "msg" => "Error opening database");
                $this->response($this->json($error), 500);
                return;
			}

			$result = $conn->query("SELECT * FROM ACCOUNT WHERE SYSTEM_ID = '$system_id'");
			if ($result->num_rows > 0) {
				if ($row = $result->fetch_array(MYSQL_ASSOC)) {
					$base64 = $row["CONFIG"];
                    $jsonString = base64_decode($base64);
                    $this->response($jsonString, 200);
				}
			}
			else
			{
                $error = array('status' => "failed", "msg" => "No account found");
                $this->response($this->json($error), 406);
			}
			$result->close();
			$conn->close();
			return;
		}
        else
        {
            $error = array('status' => "failed", "msg" => "Invalid system id");
            $this->response($this->json($error), 406);
        }
	}
	
    private function refresh_config()
    {
        if(!isset($_REQUEST['system_id'])){
            $error = array('status' => "failed", "msg" => "System ID missing in API");
            $this->response($this->json($error), 406);        
        }
        
		$system_id= $this->_request['system_id'];
		
		if(!empty($system_id))
		{
            $jsonString = file_get_contents("php://input");
            
            if (empty($jsonString))
            {
                $error = array('status' => "failed", "msg" => "Config missing in API");
                $this->response($this->json($error), 406);
                return;
            }
             
			$conn = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB);
			if ($conn->connect_error) {
                $error = array('status' => "failed", "msg" => "Error opening database");
                $this->response($this->json($error), 500);
				return;
			}

            $jsonBase64 = base64_encode($jsonString);
            #error_log($jsonBase64);
			if ($conn->query("UPDATE ACCOUNT SET CONFIG = '$jsonBase64' WHERE SYSTEM_ID = '$system_id'")) {
                $success = array('status' => "success", "msg" => "Config updated");
                $this->response($this->json($success), 200);                
            }
            else {
                $error = array('status' => "failed", "msg" => "Error updating config");
                $this->response($this->json($error), 500);
                return;                
            }
            
			$conn->close();
		}
        else
        {
            // If invalid inputs "Bad Request" status message and reason
            $error = array('status' => "failed", "msg" => "Invalid system ID in API");
            $this->response($this->json($error), 406);
        }
        return;
    }
    
	private function set_config()
	{
        if(!isset($_REQUEST['system_id'])){
            $error = array('status' => "failed", "msg" => "System ID missing in API");
            $this->response($this->json($error), 406);        
        }
        
		$system_id= $this->_request['system_id'];
		
		if(!empty($system_id))
		{
            $jsonString = file_get_contents("php://input");
            
            if (empty($jsonString))
            {
                $error = array('status' => "failed", "msg" => "Config missing in API");
                $this->response($this->json($error), 406);
                return;
            }
             
			$conn = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB);
			if ($conn->connect_error) {
                $error = array('status' => "failed", "msg" => "Error opening database");
                $this->response($this->json($error), 500);
				return;
			}

            $jsonBase64 = base64_encode($jsonString);
            $timestamp = date('Y-m-d H:i:s');

            #error_log($jsonBase64);
			//if ($conn->query("UPDATE ACCOUNT SET CONFIG = '$jsonBase64' LAST_UPDATED = $timestamp WHERE SYSTEM_ID = '$system_id'")) {
            if ($conn->query("UPDATE ACCOUNT SET CONFIG = '$jsonBase64' WHERE SYSTEM_ID = '$system_id'")) {
                $success = array('status' => "success", "msg" => "Config updated");
                $this->response($this->json($success), 200);                
            }
            else {
                $error = array('status' => "failed", "msg" => "Error updating config");
                $this->response($this->json($error), 500);
                return;                
            }
            
			$conn->close();
		}
        else
        {
            // If invalid inputs "Bad Request" status message and reason
            $error = array('status' => "failed", "msg" => "Invalid system ID in API");
            $this->response($this->json($error), 406);
        }
        return;
	}	

	private function set_command()
	{
		$system_id= $this->_request['system_id'];
		
		if(!empty($system_id))
		{
			$conn = new mysqli(self::DB_SERVER, self::DB_USER, self::DB_PASSWORD, self::DB);
			if ($conn->connect_error) {
				$this->response('', 500);
				return;
			}
			
			$jsonString = file_get_contents("php://input");
			#error_log($jsonString);
			$json_array = json_decode($jsonString, true);
			foreach($json_array as $json){
				$switch_id = $json['switch_id'];
				$current_cmd = $json['current_cmd'];
				$conn->query("UPDATE switch SET current_cmd=$current_cmd WHERE system_id = $system_id");
			}			
			$conn->close();
			$this->response('', 200);
			return;
		}
		// If invalid inputs "Bad Request" status message and reason
		$this->response('', 400);		
	}	
	
	//Encode array into JSON
	private function json($data)
	{
		if(is_array($data)){
			return json_encode($data);
		}
	}
}

//error_log(print_r($_REQUEST, true));
// Initilize Library
$api = new API;
$api->processApi();
//echo "************* Hello world !!!"

/*$conn = new mysqli(DB_SERVER, DB_USER, DB_PASSWORD, DB);
// Check connection
if ($conn->connect_error)
{
    echo "Connection error</br>";
}
else
{
    echo "Connection successful</br>";
}*/

/*$result = $conn->query("SELECT * FROM ACCOUNT");
if ($result->num_rows > 0) {
    $myArray = array();
    while($row = $result->fetch_array(MYSQL_ASSOC)) {
        echo $row['ID'] . " " . $row['EMAIL'] . "<br>";
    }
}
else
{
    echo "Query error";
}
*/

/*if ($conn->query("ALTER TABLE ACCOUNT ADD COLUMN JSON LONGTEXT")) {
    echo "Table altered</br>";
} else {
    echo "Failed to alter table</br>";
}*/

//$conn->close();

?>
