
function createMajiang()
{
	majiang = [];
	for(i=0;i<9;i++)
	{
		for(k=0;k<4;k++)
		{
			majiang.push(createPai("tong",i+1));
			majiang.push(createPai("tiao",i+1));
			majiang.push(createPai("wan",i+1));
		}
	}
	return majiang;
}

function createPai(theType,num)
{
	bian = [];
	if(num == 1)
	{
		bian.push(2);
	}
	else if(num == 9)
	{
		bian.push(8);
	}
	else
	{
		bian.push(num+1);
		bian.push(num-1);
	}
	return {type:theType,num:num,bian:bian}
}

function sasaizi()
{
	return Math.round(Math.random()*11) + 1;
}

function xipai(majiang)
{
	majiang2 = [];
	
	for(i=0;i<108;i++)
	{
		k = Math.round(Math.random()*(majiang.length-1));
		f = majiang[k];
		majiang.splice(k,1);
		majiang2.push(f);
	}
	
	return majiang2;
}

function suiji13(majiang)
{
	yipai = [];
	for(i=0;i<13;i++)
	{
		k = Math.round(Math.random()*(majiang.length-1));
		f = majiang[k];
		majiang.splice(k,1);
		yipai.push(f);
	}
	return yipai;
}

function paixu(yipai)
{
	yipai2 = [];
	pai_tong = [];
	pai_tiao = [];
	pai_wan = [];
	for(i=0;i<yipai.length;i++)
	{
		yi = yipai[i];
		if(yi.type=="tong")
		{
			pai_tong.push(yi);
		}
		else if(yi.type=="tiao"){
			pai_tiao.push(yi);
		}
		else
		{
			pai_wan.push(yi);
		}
	}
	pai_tong.sort(function(a,b){
		return a.num - b.num;
	});
	pai_tiao.sort(function(a,b){
		return a.num - b.num;
	});
	pai_wan.sort(function(a,b){
		return a.num - b.num;
	});
	yipai2['tong'] = pai_tong;
	yipai2['tiao'] = pai_tiao;
	yipai2['wan'] = pai_wan;
	return yipai2;
}

function ifjiao(yipai)
{
	
}


majiang = createMajiang();
majiang2 = xipai(majiang);
yipai3 = suiji13(majiang2);
yipai = paixu(yipai3);
console.log(yipai);

