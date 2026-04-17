#cloud
- format change: just set N/A, no need crawl
- date fix: year only to YYYY-MM-DD
- one book frontcover issue:
url:
https://www.ebookservice.tw/ntl2/book/2cd736d5-a926-4381-8674-07a26f0e6170

fix: has multiple duplicate frontcover

#ntl
- source change: set Platform_Name only
- author, date, format in document.querySelector("#bookdetailcpcontentblock")
    - author: "作者： "<a href>[author]</a>
    - date: "出版年： [date][民xxx]", date is year only, xxx=date-1911
    - format: "物件類型： [format]"
    - frontcover: <figure><img...src="[frontcover]">
#udn
- date: 
search date in the HTML contains the literal string "出版日期 [date]" by YYYY-MM-DD 

#hyread
design consider: its information update take more time. need solution like get and extract data for available platforms in parallel pipeline