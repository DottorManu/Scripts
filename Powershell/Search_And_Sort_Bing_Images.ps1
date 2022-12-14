#Takes all downloaded images, searches them on website and finds to which year/month they belong to
$files = Get-ChildItem -Recurse "C:\Users\Admin\Downloads\img" | Where { ! $_.PSIsContainer } | Select Name,FullName
$wc = New-Object System.Net.WebClient

foreach($file in $files) {
    $name = [io.path]::GetFileNameWithoutExtension($file.Name)
	$search_url = "https://www.bwallpaperhd.com/?s=$name"
	$links = ((Invoke-WebRequest –Uri $search_url).Links | Select -ExpandProperty href) | Select-Object -Unique
	$link = ($links | where {$_ -match '.html' -and $_ -notMatch  'popular-' -and $_ -notMatch  'random-' -and $_ -notMatch  'sitemap'})
	if(($link.length -gt 1) -And ($link.length -lt 10)){
		$link = $link[0]
	}
	$page = ((Invoke-WebRequest –Uri $link).Links | Select-Object -ExpandProperty href)| where {$_ -match '.jpg'} | Select-Object -Unique
	$final_url = ($page | Sort-Object { $_.length })[0]
	$year = ($final_url -split "/")[-3]
	$month = ($final_url -split "/")[-2]

	Write-Output "$name belongs to $year/$month"
}