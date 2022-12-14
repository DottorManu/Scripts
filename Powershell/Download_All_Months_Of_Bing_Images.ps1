#Downloads every image from https://www.bwallpaperhd.com
$start_year = 2010
$end_year = 2022
function Get-Image ($final_url) {
	$img_name = ($final_url -split "/")[-1]
	$folder = ($final_url -split "/")[-3] + "/" + ($final_url -split "/")[-2]
	New-Item -ItemType directory -Force -Path $folder | Out-Null
	$path = "$folder/$img_name"
	$wc.DownloadFile($final_url, $path)
	Write-Output "    $img_name"
}

function Fetch-ImgLinks($imglinks){
	foreach($link in $imglinks) {
		$page = ((Invoke-WebRequest –Uri $link).Links | Select-Object -ExpandProperty href)| where {$_ -match '.jpg'} | Select-Object -Unique
		$final_url = ($page | Sort-Object { $_.length })[0]
		Get-Image ($final_url)
	}
}
function Fetch-Page($page){
	$all_links = ((Invoke-WebRequest –Uri $page).Links | Select-Object -ExpandProperty href) | Select-Object -Unique
	$imglinks = $all_links | where {$_ -match '.html' -and $_ -notMatch  'popular-' -and $_ -notMatch  'random-' -and $_ -notMatch  'sitemap'}
	Fetch-ImgLinks($imglinks)
}
function Fetch-Month($month){
	$page = "https://www.bwallpaperhd.com/$year/$month"
	Fetch-Page($page)
	$all_links = ((Invoke-WebRequest –Uri $page).Links | Select-Object -ExpandProperty href) | Select-Object -Unique
	$other_pages = $all_links | where {$_ -match '/page/'}
	if($other_pages.length -eq 0){
		return  
	}
	$last_page = (($other_pages[-1]) -split "/")[-1]
	for($i = 2; $i -le $last_page; $i++){ 
		$page = "https://www.bwallpaperhd.com/$year/$month/page/$i"
		Fetch-Page($page)
	}
}


$wc = New-Object System.Net.WebClient
for($year = $start_year; $year -le $end_year; $year++){ 
	for($m = 1; $m -lt 13; $m++){ 
		$month = "{0:D2}" -f $m
		Write-Output "Downloading: $year/$month"
		Fetch-Month($month)
	}
}