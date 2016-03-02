<?php

require_once("Rest.inc.php");

class API extends REST 
{
	public $data = "";
	const DB_SERVER = "localhost";
	const DB_USER = "u627812499_admin";
	const DB_PASSWORD = "password";
	const DB = "u627812499_db";

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
				$func == "add_module" ||
				$func == "add_switch" ||
				$func == "set_status" ||
				$fund == "set_command")
			{
				// Cross validation if the request method is POST else it will return "Not Acceptable" status
				if($this->get_request_method() != "POST")
				{
					$error = array('status' => "failed", "msg" => "Use POST request");
					$this->response($this->json($error), 406);
					return;
				}
			}
			if ($func == "get_status" ||
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
		$controller_id = $this->_request['controller_id'];
		$total_module = $this->_request['total_module'];
		
		// Input validations
		if(!empty($email) and !empty($controller_id) and !empty($total_module))
		{
			if(filter_var($email, FILTER_VALIDATE_EMAIL))
			{
				$conn = new mysqli(self::DB_SERVER, self::DB_USER, self::DB_PASSWORD, self::DB);
				// Check connection
				if ($conn->connect_error) {
					$error = array('status' => "failed", "msg" => "Error opening database");
					$this->response($this->json($error), 500);
					return;
				}
				
				if ($conn->query("INSERT INTO ACCOUNT (EMAIL, CONTROLLER_ID, TOTAL_MODULE) VALUES ('$email', '$controller_id', '$total_module')") === TRUE)
				{
					$success = array('status' => "success", "msg" => "Record created successfully");
					$this->response($this->json($success), 200);
				}
				else
				{
					$error = array('status' => "failed", "msg" => "Error inserting new record in ACCOUNT");
					$this->response($this->json($error), 400);
				}
				$conn->close();
			}
			return;
		}

		// If invalid inputs "Bad Request" status message and reason
		$error = array('status' => "failed", "msg" => "Invalid email or controller_id or total_module");
		$this->response($this->json($error), 400);
	}

	private function add_module()
	{
		$controller_id = $this->_request['controller_id'];
		$module_id = $this->_request['module_id'];
		$total_switch = $this->_request['total_switch'];
		
		// Input validations
		if(!empty($controller_id) and !empty($module_id) and !empty($total_switch))
		{
			$conn = new mysqli(self::DB_SERVER, self::DB_USER, self::DB_PASSWORD, self::DB);
			// Check connection
			if ($conn->connect_error) {
				$error = array('status' => "failed", "msg" => "Error opening database");
				$this->response($this->json($error), 500);
				return;
			}
			
			if ($conn->query("INSERT INTO CONTROLLER (CONTROLLER_ID, MODULE_ID, TOTAL_SWITCH) VALUES ('$controller_id', '$module_id', '$total_switch')") === TRUE)
			{
				$success = array('status' => "success", "msg" => "Record created successfully");
				$this->response($this->json($success), 200);
			}
			else
			{
				$error = array('status' => "failed", "msg" => "Error inserting new record in ACCOUNT");
				$this->response($this->json($error), 400);
			}
			$conn->close();
			return;
		}

		// If invalid inputs "Bad Request" status message and reason
		$error = array('status' => "failed", "msg" => "Invalid controller_id or module_id or total_switch");
		$this->response($this->json($error), 400);		
	}

	private function add_switch()
	{
		$module_id = $this->_request['module_id'];
		$switch_id = $this->_request['switch_id'];
		$status = $this->_request['status'];
		
		// Input validations
		if(!empty($module_id) and !empty($switch_id) and !empty($status))
		{
			$conn = new mysqli(self::DB_SERVER, self::DB_USER, self::DB_PASSWORD, self::DB);
			// Check connection
			if ($conn->connect_error) {
				$error = array('status' => "failed", "msg" => "Error opening database");
				$this->response($this->json($error), 500);
				return;
			}
			
			if ($conn->query("INSERT INTO MODULE (MODULE_ID, SWITCH_ID, STATUS) VALUES ('$module_id', '$switch_id', '$status')") === TRUE)
			{
				$success = array('status' => "success", "msg" => "Record created successfully");
				$this->response($this->json($success), 200);
			}
			else
			{
				$error = array('status' => "failed", "msg" => "Error inserting new record in ACCOUNT");
				$this->response($this->json($error), 400);
			}
			$conn->close();
			return;
		}

		// If invalid inputs "Bad Request" status message and reason
		$this->response('', 400);		
	}
	
    private function endsWith( $str, $sub )
    {
        return ( substr( $str, strlen( $str ) - strlen( $sub ) ) === $sub );
    }
	private function getSystemStatus()
	{
        $host    = "127.0.0.1";
        $port    = 9999;
        $message = "{\"command\": \"getStatus\"}\r\n";
        $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
        socket_connect($socket, $host, $port) or die("Could not connect to server\n");  
        socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
        $result = '';
        while (endsWith("\r\n") == false)
        {
            $result += socket_read ($socket, 1024) or die("Could not read server response\n");
        }
        
        #echo "Reply From Server  :".$result;
        // close socket
        socket_close($socket);    
        $this->response($result, 200);
        
        /*$myfile = fopen("../config/system.json", "r") or die("Unable to open file!");
        $config = fread($myfile, filesize("../config/system.json"));
        fclose($myfile);
        $this->response($config, 200);*/
	}
	
	private function get_status()
	{
		$system_id= $this->_request['system_id'];
		
		if(!empty($system_id))
		{
			$conn = new mysqli(self::DB_SERVER, self::DB_USER, self::DB_PASSWORD, self::DB);
			// Check connection
			if ($conn->connect_error) {
				$this->response('', 500);
				return;
			} 

			$result = $conn->query("SELECT * FROM switch WHERE system_id= $system_id");
			if ($result->num_rows > 0) {
				$myArray = array();
				while($row = $result->fetch_array(MYSQL_ASSOC)) {
					$myArray[] = $row;
				}
				$this->response($this->json($myArray), 200);
			}
			else
			{
				$this->response('',204); // If no records "No Content" status			
			}
			$result->close();
			$conn->close();
			return;
		}
		// If invalid inputs "Bad Request" status message and reason
		$this->response('', 400);		
	}
	
	private function set_status()
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
			error_log($jsonString);
			$json_array = json_decode($jsonString, true);
			foreach($json_array as $json){
				$switch_id = $json['switch_id'];
				$status = $json['status'];
				$conn->query("UPDATE switch SET status=$status WHERE system_id=$system_id AND switch_id=$switch_id");
			}
			$conn->close();
			$this->response('', 200);
			return;
		}
		// If invalid inputs "Bad Request" status message and reason
		$this->response('', 400);		
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
			error_log($jsonString);
			$json_array = json_decode($jsonString, true);
			foreach($json_array as $json){
				$switch_id = $json['switch_id'];
				$current_cmd = $json['current_cmd'];
				$conn->query("UPDATE switch SET current_cmd=$current_cmd WHERE system_id=$system_id AND switch_id=$switch_id");
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


// Initiiate Library
$api = new API;
$api->processApi();

?>
