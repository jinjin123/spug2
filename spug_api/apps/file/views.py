# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
import xlwt
from django.shortcuts import HttpResponse
from libs.utils import host_select_args,host_select_cns,get_data
from django.views.generic import View
from django_redis import get_redis_connection
from apps.host.models import *
from apps.config.models import *
from apps.file.utils import FileResponseAfter, parse_sftp_attr
from libs import json_response, JsonParser, Argument
from functools import partial
import os
from libs.pwd import encryptPwd,decryptPwd
import ast
from django.db.models import Q

class FileView(View):
    def get(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='参数错误'),
            Argument('path', help='参数错误')
        ).parse(request.GET)
        if error is None:
            if not request.user.has_host_perm(form.id):
                return json_response(error='无权访问主机，请联系管理员')
            host = Host.objects.get(pk=form.id)
            if not host:
                return json_response(error='未找到指定主机')
            cli = host.get_ssh()
            objects = cli.list_dir_attr(form.path)
            return json_response([parse_sftp_attr(x) for x in objects])
        return json_response(error=error)


class ObjectView(View):
    def get(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='参数错误'),
            Argument('file', help='请输入文件路径')
        ).parse(request.GET)
        if error is None:
            if not request.user.has_host_perm(form.id):
                return json_response(error='无权访问主机，请联系管理员')
            host = Host.objects.filter(pk=form.id).first()
            if not host:
                return json_response(error='未找到指定主机')
            filename = os.path.basename(form.file)
            cli = host.get_ssh().get_client()
            sftp = cli.open_sftp()
            f = sftp.open(form.file)
            return FileResponseAfter(cli.close, f, as_attachment=True, filename=filename)
        return json_response(error=error)

    def post(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='参数错误'),
            Argument('token', help='参数错误'),
            Argument('path', help='参数错误'),
        ).parse(request.POST)
        if error is None:
            if not request.user.has_host_perm(form.id):
                return json_response(error='无权访问主机，请联系管理员')
            file = request.FILES.get('file')
            if not file:
                return json_response(error='请选择要上传的文件')
            host = Host.objects.get(pk=form.id)
            if not host:
                return json_response(error='未找到指定主机')
            cli = host.get_ssh()
            rds_cli = get_redis_connection()
            callback = partial(self._compute_progress, rds_cli, form.token, file.size)
            cli.put_file_by_fl(file, f'{form.path}/{file.name}', callback=callback)
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='参数错误'),
            Argument('file', help='请输入文件路径')
        ).parse(request.GET)
        if error is None:
            if not request.user.has_host_perm(form.id):
                return json_response(error='无权访问主机，请联系管理员')
            host = Host.objects.get(pk=form.id)
            if not host:
                return json_response(error='未找到指定主机')
            cli = host.get_ssh()
            cli.remove_file(form.file)
        return json_response(error=error)

    def _compute_progress(self, rds_cli, token, total, value, *args):
        percent = '%.1f' % (value / total * 100)
        rds_cli.lpush(token, percent)
        rds_cli.expire(token, 300)

class Exceldown(View):

    def get(self,request,type):
        if type == "host":
            if not os.path.exists('./upload/'):
                os.makedirs('./upload/')
            connecbase = ','
            connecstr = connecbase.join(host_select_args)
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format("资产信息汇总" + '.xls').encode('gb2312')
            write_data_to_excel("./upload/", "资产信息汇总", "select " + connecstr + " from hosts",host_select_args ,host_select_cns)
            full_path = os.path.join('./upload/', "资产信息汇总"+ '.xls')
            if os.path.exists(full_path):
                response['Content-Length'] = os.path.getsize(full_path)  # 可不加
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="%s.xls"' % "资产信息汇总"
                content = open(full_path, 'rb').read()
                response.write(content)
                return response

    def post(self,request,type):
        form, error = JsonParser(
            Argument('data', type=list, required=False),
            # Argument('child_project', type=list, required=False),
            # Argument('zone', type=list, required=False),
            # Argument('otp', type=str, required=False),
            # Argument('provider', type=str, required=False),
            # Argument('cluster', type=list, required=False),
            # Argument('work_zone', type=int, required=False),
            # Argument('f_ip', type=list, required=False),
        ).parse(request.body)
        if error is None:
            tmp = []
            for x in form.data:
                 tmp.append(x["id"])
            if len(tmp) > 0 and len(tmp) ==1:
                if type == "host":
                    if not os.path.exists('./upload/'):
                        os.makedirs('./upload/')
                    connecbase = ','
                    connecstr = connecbase.join(host_select_args)
                    response = HttpResponse()
                    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("资产信息汇总" + '.xls').encode(
                        'gb2312')
                    write_data_to_excel("./upload/", "资产信息汇总", "select " + connecstr + " from hosts  where id in {}".format(','.join('({})'.format(t) for t in tmp)), host_select_args,
                                        host_select_cns)
                    full_path = os.path.join('./upload/', "资产信息汇总" + '.xls')
                    if os.path.exists(full_path):
                        response['Content-Length'] = os.path.getsize(full_path)  # 可不加
                        response['Content-Type'] = 'application/octet-stream'
                        response['Content-Disposition'] = 'attachment;filename="%s.xls"' % "资产信息汇总"
                        content = open(full_path, 'rb').read()
                        response.write(content)
                        return response
            elif len(tmp) > 1:
                if type == "host":
                    if not os.path.exists('./upload/'):
                        os.makedirs('./upload/')
                    connecbase = ','
                    connecstr = connecbase.join(host_select_args)
                    response = HttpResponse()
                    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("资产信息汇总" + '.xls').encode(
                        'gb2312')
                    write_data_to_excel("./upload/", "资产信息汇总", "select " + connecstr + " from hosts  where id in {}".format(tuple(tmp)), host_select_args,
                                        host_select_cns)
                    full_path = os.path.join('./upload/', "资产信息汇总" + '.xls')
                    if os.path.exists(full_path):
                        response['Content-Length'] = os.path.getsize(full_path)  # 可不加
                        response['Content-Type'] = 'application/octet-stream'
                        response['Content-Disposition'] = 'attachment;filename="%s.xls"' % "资产信息汇总"
                        content = open(full_path, 'rb').read()
                        response.write(content)
                        return response

            return json_response(error="")


class DbmExceldown(View):

    def get(self,request,type):
        if type == "host":
            if not os.path.exists('./upload/'):
                os.makedirs('./upload/')
            connecbase = ','
            connecstr = connecbase.join(host_select_args)
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format("资产信息汇总" + '.xls').encode('gb2312')
            write_data_to_excel("./upload/", "资产信息汇总", "select " + connecstr + " from multidb",host_select_args ,host_select_cns)
            full_path = os.path.join('./upload/', "资产信息汇总"+ '.xls')
            if os.path.exists(full_path):
                response['Content-Length'] = os.path.getsize(full_path)  # 可不加
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="%s.xls"' % "资产信息汇总"
                content = open(full_path, 'rb').read()
                response.write(content)
                return response

    def post(self,request,type):
        form, error = JsonParser(
            Argument('data', type=list, required=False),
            # Argument('child_project', type=list, required=False),
            # Argument('zone', type=list, required=False),
            # Argument('otp', type=str, required=False),
            # Argument('provider', type=str, required=False),
            # Argument('cluster', type=list, required=False),
            # Argument('work_zone', type=int, required=False),
            # Argument('f_ip', type=list, required=False),
        ).parse(request.body)
        if error is None:
            tmp = []
            for x in form.data:
                 tmp.append(x["id"])
            if len(tmp) > 0 and len(tmp) ==1:
                if type == "host":
                    if not os.path.exists('./upload/'):
                        os.makedirs('./upload/')
                    connecbase = ','
                    connecstr = connecbase.join(host_select_args)
                    response = HttpResponse()
                    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("资产信息汇总" + '.xls').encode(
                        'gb2312')
                    write_data_to_excel("./upload/", "资产信息汇总", "select " + connecstr + " from multidb  where id in {}".format(','.join('({})'.format(t) for t in tmp)), host_select_args,
                                        host_select_cns)
                    full_path = os.path.join('./upload/', "资产信息汇总" + '.xls')
                    if os.path.exists(full_path):
                        response['Content-Length'] = os.path.getsize(full_path)  # 可不加
                        response['Content-Type'] = 'application/octet-stream'
                        response['Content-Disposition'] = 'attachment;filename="%s.xls"' % "资产信息汇总"
                        content = open(full_path, 'rb').read()
                        response.write(content)
                        return response
            elif len(tmp) > 1:
                if type == "host":
                    if not os.path.exists('./upload/'):
                        os.makedirs('./upload/')
                    connecbase = ','
                    connecstr = connecbase.join(host_select_args)
                    response = HttpResponse()
                    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("资产信息汇总" + '.xls').encode(
                        'gb2312')
                    write_data_to_excel("./upload/", "资产信息汇总", "select " + connecstr + " from multidb  where id in {}".format(tuple(tmp)), host_select_args,
                                        host_select_cns)
                    full_path = os.path.join('./upload/', "资产信息汇总" + '.xls')
                    if os.path.exists(full_path):
                        response['Content-Length'] = os.path.getsize(full_path)  # 可不加
                        response['Content-Type'] = 'application/octet-stream'
                        response['Content-Disposition'] = 'attachment;filename="%s.xls"' % "资产信息汇总"
                        content = open(full_path, 'rb').read()
                        response.write(content)
                        return response

            return json_response(error="")



def write_data_to_excel(fpath,name,sql,header,header_cns):
    import ast
    result = get_data(sql)
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    # 遍历result中的没个元素。
    for i in range(len(header_cns)):
        sheet.write(0, i, header_cns[i])
    for i in range(len(result)):
        data_dict = dict(zip(header, result[i]))
        for index, key in enumerate(header):
            if key =="data_disk":
                tt = ""
                if data_dict[key] != "[]" and  data_dict[key] is not None:
                    for x in ast.literal_eval(data_dict[key]):
                        tt += "数据盘:" + x.get("name") + ";容量:" + str(x.get("size")) + "G;"
                # for x in ast.literal_eval(data_dict[key]):
                    # tt += u"类型:" + x.get("type") + u",数据盘:" + x.get("name") + u",挂载目录:" + x.get("mount") + u",总大小:" + str(
                    #     x.get("total_szie")) + u"G,数据盘已使用" + str(x.get("used")) + u"G,"
                sheet.write(i + 1, index, tt)
            elif key == "sys_disk":
                tt = ""
                if data_dict[key] != "[]" and  data_dict[key] is not None:
                    for x in ast.literal_eval(data_dict[key]):
                        tt = "系统盘:"+ x["name"] +";容量:" + str(x.get("total_size")) + "G;"
                # for x in ast.literal_eval(data_dict[key]):
                    # tt += u"类型:" + x.get("type") + u",数据盘:" + x.get("name") + u",挂载目录:" + x.get("mount") + u",总大小:" + str(
                    #     x.get("total_szie")) + u"G,数据盘已使用" + str(x.get("used")) + u"G,"
                sheet.write(i + 1, index, tt)
            elif key == "status":
                if data_dict[key] == 0:
                    sheet.write(i + 1, index, "在线")
                else:
                    sheet.write(i + 1, index, "离线")
            elif key == "env_id":
                if data_dict[key] == 2:
                    sheet.write(i + 1, index, "生产")
                else:
                    sheet.write(i + 1, index, "测试")
            elif key == "password_hash":
                if data_dict[key]:
                    sheet.write(i + 1, index,decryptPwd(data_dict[key]))
            elif key == "top_project":
                tt = []
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    for x in ast.literal_eval(data_dict[key]):
                        tt.append((ProjectConfig.objects.get(pk=x)).name)
                    ttt = ";".join(tt)
                sheet.write(i + 1, index, ttt)
            elif key == "child_project":
                tt = []
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    for x in ast.literal_eval(data_dict[key]):
                        tt.append((ProjectConfig.objects.get(pk=x)).name)
                    ttt = ";".join(tt)
                sheet.write(i + 1, index, ttt)
            elif key == "cluster":
                tt = []
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    for x in ast.literal_eval(data_dict[key]):
                        tt.append((ClusterConfig.objects.get(pk=x)).name)
                    ttt = ";".join(tt)
                sheet.write(i + 1, index, ttt)
            elif key == "zone":
                tt = []
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    for x in ast.literal_eval(data_dict[key]):
                        tt.append((Zone.objects.get(pk=x)).name)
                    ttt = ";".join(tt)
                sheet.write(i + 1, index, ttt)
            elif key == "service_pack":
                tt = []
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    for x in ast.literal_eval(data_dict[key]):
                        tt.append((Servicebag.objects.get(pk=x)).name)
                    ttt = ";".join(tt)
                sheet.write(i + 1, index, ttt)
            elif key == "provider":
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    ttt = (DevicePositon.objects.get(pk=data_dict[key]).name)
                sheet.write(i + 1, index, ttt)
            elif key == "resource_type":
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    ttt = (ResourceType.objects.get(pk=data_dict[key]).name)
                sheet.write(i + 1, index, ttt)
            elif key == "username":
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    ttt = (ConnctUser.objects.get(pk=data_dict[key]).name)
                sheet.write(i + 1, index, ttt)
            elif key == "work_zone":
                ttt = ""
                if data_dict[key] != "[]" and data_dict[key] is not None:
                    ttt = (WorkZone.objects.get(pk=data_dict[key]).name)
                sheet.write(i + 1, index, ttt)

            elif key == "dbrelation":
                if data_dict[key] == 1:
                    sheet.write(i + 1, index, "主")
                if data_dict[key] == 2:
                    sheet.write(i + 1, index, "从")
                if data_dict[key] == 3:
                    sheet.write(i + 1, index, "集群")
                if data_dict[key] == 4:
                    sheet.write(i + 1, index, "无")
            else:
                sheet.write(i + 1, index, data_dict[key])
    wbk.save(fpath + name + '.xls')