(function (){
	var gotop = $('#gotop'),
		contactonline = $('#contactonline'),
		contact_wrap = $('.contact-wrap'),
		dl_btn = $('.site-dl'),
		login_page = $('.login-page'),
		dl_box = $('.dl-box'),
		dl_close = $('.dl-close'),
		dl_uname = $('.dl-empty').eq(0),
		dl_upw = $('.dl-empty').eq(1),
		dl_push = $('.dl-push'),
		dl_ts = $('.dl-ts-txt'),
		is_authenticated = $('.is_authenticated'),
		_remeber = document.getElementById('remeber_us');

	is_authenticated.on('click',function (){

		// get Cookie
		var uphone = getCookie('uphone');
		dl_uname.val(uphone);

		login_page.fadeIn();
		return false;
	});

	// goTop
	$(window).scroll(function (){
		if($(window).scrollTop() > 700){
			gotop.fadeIn();
		}else {
			gotop.fadeOut();
		}
	});

	gotop.on('click',function (){
		$('body').animate({'scrollTop':0});
	});

	// contactonline
	contactonline.on('click',function (){
		var screenHeight = window.screen.height,
			screenWidth = window.screen.width,
			winHeight = 587,
			winWidth = 800,
			winTop = (screenHeight-587)/2-100,
			winLeft = (screenWidth-800)/2;
		console.log('screen:'+screenHeight+'/'+screenWidth);
		window.open ('/shop/chat_customer_service_win','chatToService','height='+winHeight+',width='+winWidth+',top='+winTop+',left='+winLeft+',toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');
	});

	// 登陆部分
	dl_btn.on('click',function (){

		// get Cookie
		var uphone = getCookie('uphone');
		dl_uname.val(uphone);

		login_page.fadeIn();
	});

	dl_close.on('click',function (){
		login_page.fadeOut();
	});

	dl_uname.on('blur',function (){
		var uname = dl_uname.val();

		$.post('/account/check_phone',{'phone':uname},function (e){
			result = JSON.parse(e);

			if(result['status']=='TRUE'){
				dl_ts.text('');
			}else {
				dl_ts.text('手机号不存在或者未注册');
			}
		});

	});

	dl_push.on('click',function (){
		Login();
	});

	dl_box.on('keyup',function (e){
		if(e.keyCode == 13){
			Login();
		}
	});

	// 登陆方法
	function Login(){
		var uname = dl_uname.val(),
			upw = dl_upw.val();

		if(uname =='' || uname == null){
			dl_ts.text('账号/密码不能为空');
		}else {
			$.post('/account/u_login',{'phone':uname,'password':upw},function (e){
				result = JSON.parse(e);
				if (result['status'] == 'FAILURE'){
					dl_ts.text('账户密码错误');
				}else{
					if(_remeber.checked){
						addCookie('uphone', uname, 10);
					}
					location.reload();
				}
			});
		}

	}

	// 设置 cookie
	function addCookie(name, value, expiresDays){ 
		var cookieString = name + "=" + escape(value);

		// 判断是否设置过期时间
		if(expiresDays>0){
			var date=new Date();
			date.setTime(date.getTime + expiresDays*24*3600*1000);
			cookieString = cookieString + "; expires=" + date.toGMTString();
		}
		document.cookie = cookieString;
	}

	// 获取 cookie
	function getCookie(name){
		var strCookie = document.cookie,
			arrCookie = strCookie.split("; ");

		for(var i=0;i<arrCookie.length;i++){
			var arr = arrCookie[i].split("=");
			if(arr[0] == name) return arr[1];
		}
		return "";
	}

}())
