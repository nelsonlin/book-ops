Use search 'python' as example

#Extract source and url by logic
##Search result 1st page: https://taiwanlibrarysearch.herokuapp.com/result?book=python

- [Platform_num]=1/2/3/4
- [Platform_Name]=HYREAD/UDN/國立公共資訊圖書館/台灣雲端書庫 by #Selector: root > div > div.result-container > div > div:nth-child([Platform_num]) > div > div.items-head > p
- [M]th book within [N]th [Source_Library] and [URL] by #Selector: #root > div > div.result-container > div > div:nth-child([Platform_num]) > div > div.items-body > div > div > div.ui.accordion > div:nth-child(2*[M]) > div > a:nth-child([N])
<a class="item" href="[URL]" target="_blank">[Source_Libray]</a>
- [Source]=[Platform_Name]/[Source_Libray]

#Extract title, arthur, date, format, figure of [M]th book within 1th [Source_Library] and [URL]
by logic

##[Platform_num]=1
- [title] by selector:#center > div:nth-child(9) > div > div:nth-child(1) > div.col-lg-6.col-md-6.col-sm-8.col-xs-12 > div > h3
- 作者：[author]著 by selector:#center > div:nth-child(9) > div > div:nth-child(1) > div.col-lg-6.col-md-6.col-sm-8.col-xs-12 > div > p:nth-child(4)
- 出版年：[date] by selector:#center > div:nth-child(9) > div > div:nth-child(1) > div.col-lg-6.col-md-6.col-sm-8.col-xs-12 > div > p:nth-child(5)

##[Platform_num]=2
- [date] by selector:#__nuxt > div > div.mb-14.flex-grow.pt-16.lg\:pt-48 > main > div > div.mb-6.gap-10.lg\:mb-14.lg\:grid.lg\:grid-cols-\[1fr_3fr_1fr\] > div:nth-child(2) > div.lg\:hidden > div > div:nth-child(3) > p

##[Platform_num]=3
(Backlog)
##[Platform_num]=4
(Backlog)

#Mapping title, arthur, date, format, figure of [M]th book beyond 1st [Source_Library] and [URL]
- Mapping by [M]th book 1st [Source_Library] and [URL]

