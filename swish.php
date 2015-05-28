<?php
// Initiate mysqli first... (not included)


$url = "https://appserver.icabanken.se/login/passwordlogin?customerId=9508216273&password=****";
$ch = curl_init();
curl_setopt($ch,CURLOPT_HTTPHEADER,array('Accept : application/json', 'ApiKey: 8987B80B-A708-4C61-B8CF-350D4BA289F0', 'ClientAppVersion: 777', 'ClientOSVersion: 21', 'ClientOS: Android', 'ClientHardware: E975'));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_URL,$url);
$result=curl_exec($ch);
curl_close($ch);

$json = json_decode($result, true);

$trans = $json["AccountList"]["Accounts"][0]["Transactions"];


foreach($trans as $item) { 
  if ($item['HasDetails'] && isset($item['Details']['SwishAmount'])) {

	$msg = $item['Details']['SwishMessage'];
	$person = $item['Details']['SwishSenderDescription'];
	$coolguy = false;
	switch($person) {
		case "AXEL DELBOM +46 76 347 88 25":
		case "ISAK PERSSON +46 70 325 77 99":
			$coolguy = true;
			break;
	}
	if (($item['Amount'] == 7 or $coolguy) and substr(strtolower($msg), 0,4) == "fack" ){
	  $msgnospace = preg_replace('/\s+/', '', $msg);
	  if(strlen($msgnospace) < 5) break;
	  $facknr = $msgnospace[4];
	  if ($facknr > 5 || $facknr < 1) break;

	  // Kolla om ordern redan finns
	  $det = $item['Details'];
	  $ref = $det['SwishReferenceId'];

	  $testSql = "SELECT * FROM location WHERE swishref = '$ref' LIMIT 1";
	  

	  $testResult = $conn->query($testSql);
	  if($testResult->num_rows == 0) {
		$location = "F" . $facknr;
		$cost = $item['Amount'];
		$swTime = $det["SwishTime"];
		
		$sender = $det['SwishSenderDescription'];
		$swName = explode("+",$sender);
		if ( strpos($swName[0],",") ) {
			$fName = explode(",",$swName[0]);
			$swName[0] = trim($fName[1]) . " ". trim($fName[0]);
		}
		$name = strtoupper(trim($swName[0]));
		$phone = preg_replace('/\s+/', '', $swName[1]);
		
		$product = "SWISHFAIL";
		$productNameSql = "SELECT name FROM sodas WHERE fack = '$facknr' LIMIT 1";
		$productNameResult = $conn->query($productNameSql);
		if($productNameResult->num_rows > 0) {
			$product = $productNameResult->fetch_assoc()["name"];
		}
		

		$addSql = "INSERT INTO location (location,locationi,name,swishref,swishtime,message,processed,phone,cost,product) VALUES ('$location','$facknr','$name','$ref','$swTime','$msg',false,'$phone','$cost','$product')";
		$result = $conn->query($addSql);
		
		$alias = trim(explode($facknr,$msg)[1]);
		//$addSql = "SELECT l.*, a.Alias FROM alias a INNER JOIN location l ON l.phone = a.Phone"
		$addSql = "";
		if (strlen($alias) > 0) {
			$addSql = "INSERT INTO alias (`phone`,`alias`) VALUES ('$phone','$alias') ON DUPLICATE KEY UPDATE `alias`='$alias'";
		} else {
			$addSql = "INSERT INTO alias (`phone`,`alias`) VALUES ('$phone','$alias') ON DUPLICATE KEY UPDATE `phone`=`phone`";
		}
		$conn->query($addSql);
	  } else
			break;   // <- <- COOL THING!!!
	}
  }
}
?>
