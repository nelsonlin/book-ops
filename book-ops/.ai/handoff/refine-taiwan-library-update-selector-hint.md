# Update selector by HTML element mapping

Fix: Title、Author、Date、format
Add: Frontcover

# HTML element mapping
There are html element(mark by [book information item]) mapping to book information item by HTML example from SourceSite(Hyread、UDN、台灣雲端書庫、國立公共資訊圖書館)

#Hyread、UDN、台灣雲端書庫
##first page
URL、Source(=SourceSite+Source_Library): <a class="item" href="[URL]" target="_blank">[Source1_Library]</a>

#Hyread
##second page
Title: <div class="book-detail"><h3>[Title]<h3>
Author: <p class="note">作者：[Author]著</p>
Date: <p class="note">出版年：[Date]</p>
format: <p class="note">格式：[format]</p>
Frontcover:<a href="#" class="book-cover" aria-label="書封"><img src="[Frontcover]" alt=""></a>

#UDN
##second page
- Title、Author、Frontcover、Date、format:
<div class="container"><div class="my-5 flex items-center gap-1 text-sm text-secondary"><a href="/udnlib/tyccc" class="router-link-active whitespace-nowrap hover:text-primary">首頁</a><!--[--><!--[--><i class="i-arrow5-right"></i><a href="/udnlib/tyccc/classification/book" class="line-clamp-1 hover:text-primary">電子書</a><!--]--><i class="i-arrow5-right"></i><a href="/udnlib/tyccc/classification/book?category=75,76,77,78,80,82,83,85" class="line-clamp-1 hover:text-primary">資訊電腦</a><!--[--><i class="i-arrow5-right"></i><a href="/udnlib/tyccc/classification/book?category=80" class="line-clamp-1 hover:text-primary">程式設計</a><!--]--><!--]--></div><div class="mb-6 gap-10 lg:mb-14 lg:grid lg:grid-cols-[1fr_3fr_1fr]"><div><div class="relative mx-auto mb-3 w-44 drop-shadow-[0_0_4px_rgba(0,0,0,0.3)] lg:w-auto"><img class="mx-auto mb-3 aspect-[3/4] w-44 lg:w-auto hoverZoomLink" src="[Frontcover]" alt="cover"><!----></div><div class="mx-auto mb-3 w-fit"><button class="flex h-8 items-center gap-1 rounded bg-primary-lighter px-4 text-primary"><i class="i-heart-empty"></i> 加入收藏</button></div><div class="hidden bg-neutral-100 px-10 py-8 lg:block"><p class="mb-6">使用手機/平板掃描QR Code借閱前，請先下載/安裝 udn讀書館 App。</p><div class="relative aspect-square w-48"><canvas style="width:192px;height:192px;" class="mx-auto" width="288" height="288"></canvas><img class="absolute inset-0 m-auto w-10" src="/udnlib/images/udnlib-icon.png" alt="udnlib-icon"></div></div></div><div><div class="mb-5 flex flex-col gap-5 lg:mb-0 lg:gap-3"><h1 class="text-center text-lg font-bold lg:text-left">[Title]</h1><h3 class="flex flex-col items-center gap-2 lg:flex-row lg:gap-5"><div class="h-6 w-16 text-center after:inline-block after:w-full lg:text-justify">點閱數</div><span class="text-secondary">182</span></h3><h3 class="flex flex-col items-center gap-2 lg:flex-row lg:items-start lg:gap-5"><div class="h-6 w-16 shrink-0 text-center after:inline-block after:w-full lg:text-justify">作者</div><a href="/udnlib/tyccc/search?keyword=%E6%A6%AE%E6%AC%BD%E7%A7%91%E6%8A%80&amp;searchType=all&amp;assetType=paper" class="text-secondary">[Author]</a></h3><h3 class="flex flex-col items-center gap-2 lg:flex-row lg:gap-5"><div class="h-6 w-16 text-center after:inline-block after:w-full lg:text-justify">出版社</div><a href="/udnlib/tyccc/search?keyword=%E5%8D%9A%E7%A2%A9%E6%96%87%E5%8C%96&amp;searchType=all&amp;assetType=paper" class="text-secondary">博碩文化</a></h3><h3 class="flex flex-col items-center gap-2 lg:flex-row lg:gap-5"><div class="h-6 w-16 text-center after:inline-block after:w-full lg:text-justify">格式</div><span class="text-secondary">[format]</span></h3><div class="hidden h-8 gap-5 lg:flex"><div class="w-44"><button data-v-7720b9af="" class="block h-8 w-full rounded-md border px-2 tracking-wider transition-colors theme-gray line-clamp-1 active-theme-undefined">試閱</button></div><div class="w-44"><button data-v-7720b9af="" class="block h-8 w-full rounded-md border px-2 tracking-wider transition-colors theme-default line-clamp-1 active-theme-undefined">借閱</button></div></div><div class="fixed bottom-0 left-0 z-40 grid h-20 w-full grid-cols-2 items-center gap-6 bg-[#F8F8F8] px-9 shadow-[0_0_10px_rgba(0,0,0,0.3)] lg:hidden"><button data-v-7720b9af="" class="block h-8 w-full rounded-md border px-2 tracking-wider transition-colors theme-gray line-clamp-1 active-theme-undefined">試閱</button><button data-v-7720b9af="" class="block h-8 w-full rounded-md border px-2 tracking-wider transition-colors theme-default line-clamp-1 active-theme-undefined">借閱</button></div></div><div class="lg:hidden"><div class="flex flex-col gap-5"><!----><div><h3 class="text-center text-xl lg:text-left">館藏狀態</h3><div class="flex flex-col items-center lg:items-start"><p class="text-lg">桃園市立圖書館</p><!----><p class="text-secondary">可借 <span class="text-primary">2</span> 本 / 共 2 本</p></div></div><div class="flex flex-col items-center lg:items-start"><h3 class="text-lg">ISBN</h3><p class="text-secondary">9789864345731</p></div><!----><div class="flex flex-col items-center lg:items-start"><h3 class="text-lg">出版日期</h3><p class="text-secondary">[Date]</p></div>

#國立公共資訊圖書館
##first page
- Source: 國立公共資訊圖書館
##second page
- Title、Frontcover、format:
<table class="cptb">
	<tbody><tr>
		<td width="20%">
			<figure><img class="lazy" data-original="[Frontcover]" width="169" height="239" src="[Frontcover]" style=""></figure>
		</td>
		<td>
			<h1>[Title]</h1>
			<p>
				作者：
				<em class="underline">洪錦魁著</em>
				<!--<em class="underline">汪芸</em>譯 ;<em class="underline">吳健豐</em>圖!-->
			</p>	
			<p>物件類型：[format]</p>
- Date:
<div class="contBox open">
		<h1>書目資訊</h1>
		<!--<figure class="qrcode mob_hide"><img src="images/QrCodeImg.jsp?id=58333" width="148px" height="148px" alt=""><br/>Web</figure>-->
		<figure class="qrcode mob_hide" style="margin-right:30px"><img src="images/OpenAppQrCodeImg.jsp?id=58333" width="148px" height="148px" a="" alt="">
		<br>行動借書<br>請使用iLib Reader App 掃描<br>
		</figure>
		<ul id="bookdetailcpcontentblock" data-template="bookdetailcpcontenttpl">
	<li>作者： <a href="search#resultdata?search_input=%E6%B4%AA%E9%8C%A6%E9%AD%81%2C&amp;search_field=PN&amp;searchtype=0" target="_parent">洪錦魁,</a></li>
	<li>出版社： <a href="search#resultdata?search_input=%E6%B7%B1%E6%99%BA%E6%95%B8%E4%BD%8D%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%2C&amp;search_field=PU&amp;searchtype=0" target="_parent">深智數位股份有限公司,</a></li>
	<li>出版地： 臺北市 :</li>
	<li>出版年： [Date]</li>

#台灣雲端書庫
##second page
format: not available
Frontcover:<div class="cover"><img src="[Frontcover]"></div>
Title、Author、Date:
<div class="detail"><div class="actions"><div class="btns"><a href="#"><img src="/images/icon-demo.svg">試閱</a><a href="#"><img src="/images/icon-download.svg">借閱</a><span><a href="#"></a></span></div><div class="share"><span>分享</span><a href="https://www.facebook.com/share.php?u=https%3A%2F%2Fwww.ebookservice.tw%2Fntl2%2Fshare%2F9464859e-1175-4339-8e8c-839c00e4f72e" target="_blank"><img src="/images/social-fb.svg"></a><a href="https://social-plugins.line.me/lineit/share?url=https%3A%2F%2Fwww.ebookservice.tw%2Fntl2%2Fshare%2F9464859e-1175-4339-8e8c-839c00e4f72e" target="_blank"><img src="/images/social-line.svg"></a></div></div><h2>Python全面攻略</h2><hr><table><tbody><tr><td>作者</td><td><span>文/[Author]</span>

