import { min } from "lodash";

/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
let Permission = {
  isSuper: false,
  hostPerms: [],
  permissions: []
};

export let X_TOKEN;

export function updatePermissions() {
  X_TOKEN = localStorage.getItem('token');
  Permission.isSuper = localStorage.getItem('is_supper') === 'true';
  Permission.hostPerms = JSON.parse(localStorage.getItem('host_perms') || '[]');
  Permission.permissions = JSON.parse(localStorage.getItem('permissions') || '[]');
}

// 前端页面的权限判断(仅作为前端功能展示的控制，具体权限控制应在后端实现)
export function hasPermission(strCode) {
  const {isSuper, permissions} = Permission;
  // console.log(isSuper, strCode, permissions);
  if (!strCode || isSuper) return true;
  for (let or_item of strCode.split('|')) {
    if (isSubArray(permissions, or_item.split('&'))) {
      return true
    }
  }
  return false
}

export function hasHostPermission(id) {
  const {isSuper, hostPerms} = Permission;
  return isSuper || hostPerms.includes(id)
}

// 清理输入的命令中包含的\r符号
export function cleanCommand(text) {
  return text ? text.replace(/\r\n/g, '\n') : ''
}

//  数组包含关系判断
export function isSubArray(parent, child) {
  for (let item of child) {
    if (!parent.includes(item.trim())) {
      return false
    }
  }
  return true
}

// 用于替换toFixed方法，去除toFixed方法多余的0和小数点
export function trimFixed(data, bit) {
  return String(data.toFixed(bit)).replace(/0*$/, '').replace(/\.$/, '')
}

// 日期
export function human_date(date) {
  const now = date || new Date();
  let month = now.getMonth() + 1;
  let day = now.getDate();
  return `${now.getFullYear()}-${month < 10 ? '0' + month : month}-${day < 10 ? '0' + day : day}`
}

// 时间
export function human_time(date) {
  const now = date || new Date();
  const hour = now.getHours() < 10 ? '0' + now.getHours() : now.getHours();
  const minute = now.getMinutes() < 10 ? '0' + now.getMinutes() : now.getMinutes();
  const second = now.getSeconds() < 10 ? '0' + now.getSeconds() : now.getSeconds();
  return `${human_date()} ${hour}:${minute}:${second}`
}

// 生成唯一id
export function uniqueId() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16)
  });
}

export function formatDate(date, fmt = 'yyyy-MM-dd') {
  if (typeof (date) === 'number') {
      date = new Date(date)
  }
  var o = {
      "M+": date.getMonth() + 1, //月份
      "d+": date.getDate(), //日
      "h+": date.getHours(), //小时
      "m+": date.getMinutes(), //分
      "s+": date.getSeconds(), //秒
      "q+": Math.floor((date.getMonth() + 3) / 3), //季度
      "S": date.getMilliseconds() //毫秒
  }
  if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length))
  for (var k in o)
      if (new RegExp("(" + k + ")").test(fmt))
          fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)))
  return fmt
}

export function intervalTime(startTime,endTime) {
  // var timestamp=new Date().getTime(); //计算当前时间戳
  var timestamp = (Date.parse(new Date()))/1000;//计算当前时间戳 (毫秒级)
   var date1 = ""; //开始时间
  if(timestamp<startTime){
      date1=startTime;
  }else{
      date1 = timestamp; //开始时间
  }
  var date2 = endTime; //结束时间
  // var date3 = date2.getTime() - date1.getTime(); //时间差的毫秒数
  var date3 =  (date2- date1)*1000; //时间差的毫秒数
  //计算出相差天数
  var days = Math.floor(date3 / (24 * 3600 * 1000));
  //计算出小时数

  var leave1 = date3 % (24 * 3600 * 1000); //计算天数后剩余的毫秒数
  var hours = Math.floor(leave1 / (3600 * 1000));
  //计算相差分钟数
  var leave2 = leave1 % (3600 * 1000); //计算小时数后剩余的毫秒数
  var minutes = Math.floor(leave2 / (60 * 1000));

  //计算相差秒数

  var leave3 = leave2 % (60 * 1000); //计算分钟数后剩余的毫秒数
  var seconds = Math.round(leave3 / 1000);
  console.log(days + "天 " + hours + "小时 ")
  // return   days + "天 " + hours + "小时 " + minutes + " 分钟" + seconds + " 秒"
  return   days + "天 " + hours + "小时 "
}

export function getDatetime(happy) {
  var now = new Date();
  var year = now.getFullYear();       
  var month = now.getMonth() + 1;     
  var day = now.getDate();            
  var hh = now.getHours();            
  var mm = now.getMinutes();          
  var ss = now.getSeconds();          
  var clock = year + "-";
  if (month < 10)
      clock += "0";
  clock += month + "-";
  if (day < 10)
      clock += "0";
  clock += day + " ";
  // if (hh < 10)
  //     clock += "0";
  // clock += hh + ":";
  // if (mm < 10) clock += '0';
  // clock += mm + ":";
  // if (ss < 10) clock += '0';
  // clock += ss;
    if(happy==="week"){
      return clock;
    }else{
      clock += " 18:00:00 "
      return clock;
    }
  }


export function get_time_diff(time) {
  var diff = '';
  var time_diff = new Date().getTime() - time;
  // 计算相差天数  
  var days = Math.floor(time_diff / (24 * 3600 * 1000));
  if (days > 0) {
    diff += days + '天';
  }
  // 计算相差小时数  
  var leave1 = time_diff % (24 * 3600 * 1000);
  var hours = Math.floor(leave1 / (3600 * 1000));
  if (hours > 0) {
    diff += hours + '小时';
  } else {
    if (diff !== '') {
      diff += hours + '小时';
    }
  }
  // 计算相差分钟数  
  var leave2 = leave1 % (3600 * 1000);
  var minutes = Math.floor(leave2 / (60 * 1000));
  if (minutes > 0) {
    diff += minutes + '分';
  } else {
    if (diff !== '') {
      diff += minutes + '分';
    }
  }
  // 计算相差秒数  
  var leave3 = leave2 % (60 * 1000);
  var seconds = Math.round(leave3 / 1000);
  if (seconds > 0) {
    diff += seconds + '秒';
  } else {
    if (diff !== '') {
      diff += seconds + '秒';
    }
  }

  return diff;
}

export function FormatDate(now,gett) {
  var year = now.getFullYear();   //获取获取当前年份  
  var month = now.getMonth() + 1;   //获取获取当前月份
  var date = now.getDate();       //获取获取当前日期
  var hour = now.getHours();      //获取时
  var minute = now.getMinutes();  //获取分  
  var second = now.getSeconds();  //获取秒
  var milsecond = now.getMilliseconds();
  //时间格式 ：年-月-日   
  switch (gett){
    case "str":
      return year + "-" + month + "-" + date + " "+ hour+":"+minute+":"+second ;
    case "sec":
      return  year.toString()+month.toString()+date.toString()+hour.toString()+minute.toString()+second.toString()+milsecond.toString()  ;
  }

}
//计算时间差
export function GetDateDiff(startDate, endDate) {
  var startTime = new Date(Date.parse(startDate.replace(/-/g, "/"))).getTime();
  var endTime = new Date(Date.parse(endDate.replace(/-/g, "/"))).getTime();
  // console.log(startTime-endTime)
  var dates = Math.floor((startTime - endTime)) / (1000 * 60 );
  return parseInt(dates);
}

export function isWeekEnd(date){

  if( "天一二三四五六".charAt(new   Date(date).getDay())=="天" ) return true;

  if( "天一二三四五六".charAt(new   Date(date).getDay())=="六"  )  return true;

}

