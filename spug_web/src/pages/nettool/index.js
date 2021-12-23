/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Transfer, message, Alert, Input, Select, InputNumber, Button ,Switch,Icon,Tag} from 'antd';
import { http, hasPermission } from 'libs';
import hostStore from 'pages/host/store';
import { SearchForm, AuthDiv, AuthCard } from 'components';
import store from './store';
const { TextArea } = Input;
const { Option } = Select;
const children = [
    // <Option key={"SSH"} value={"SSH"}>{"SSH --- 22 端口"}</Option>,
    // <Option key={"HTTP"} value={"HTTP"}>{"HTTP --- 80 端口"}</Option>,
    // <Option key={"HTTPS"} value={"HTTPS"}>{"HTTPS --- 443端口"}</Option>

    <Option key={"telnet"} value={"telnet"}>{"telnet"}</Option>,
    <Option key={"curl"} value={"curl"}>{"curl"}</Option>

];

@observer
class NetTool extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: "none",
            hosts: [],
            apps: [],
            tpe: "str",
            wtool: null,
            inct: null,
            resp: null,
            tag: false,
        }
    }
    componentDidMount() {
        if (hostStore.records.length === 0) {
            hostStore.fetchRecords().then(
                () => this._updateRecords(hostStore.records, hostStore.pj)
            )
        } else {
            this._updateRecords(hostStore.records, hostStore.pj)
        }
    }

    _updateRecords = (records, pj) => {

        let tmp = []
        let tmpdata = []
        records.map(x => {

            pj.map(d => {
                if (x.top_project.includes(d.id)) {
                    tmp.push(d.name)
                }
            })
            x.top_project = tmp.join(":")
            tmp = []
            tmpdata.push(x)
        })

        const hosts = tmpdata.map(x => {
            return { ...x, key: x.id }
        })
        this.setState({ hosts })

    };

    changeType = (value) => {
        switch (value) {
            case "curl":
                this.setState({
                    tpe: "str",
                    wtool: "curl"
                })
                break;;
            case "telnet":
                this.setState({
                    tpe: "int",
                    wtool: "telnet"

                })
                break;;
        }
    }
    HandleSubmit = () => {
        const formData = { "tool": this.state.wtool, "input": this.state.inct, "hosts": store.hostPerms , "tag": this.state.tag}
        this.setState({loading: "block"})
        return http.post('/api/host/netcheck/', formData).then(({ resp }) => {
            
            let tmp =[]
            resp.map(item =>{
                Object.hasOwnProperty("success")
                ?
                    tmp.push(item.success)
                : Object.hasOwnProperty("failed") ?
                    tmp.push(item.failed)
                : tmp.push(JSON.stringify(item,undefined, 4))
            })
            this.setState({ "resp": tmp })
            message.success('验证成功');
            this.setState({loading: "none"})

        })
    }

    render() {
        const { tpe,resp } = this.state
        return (
            <div>
            {hasPermission('deploy.rancher.view') && (
                <div>
                    <Alert
                        closable
                        showIcon
                        type="info"
                        message="小提示"
                        style={{ width: 600, margin: '0 auto 20px', color: '#31708f !important' }}
                        description="默认调用堡垒机去19.104.50.128去诊断支持常见网络错误,
                        如自我判断后无法解决再把结果截图联系运维架构师---->李衡" />
                    <Form.Item label="自定义主机调用">
                        <Switch
                            checkedChildren="开启"
                            unCheckedChildren="关闭"
                            onChange={v => {
                                if(this.state.tpe === "cs"){
                                    this.setState({tag: v, tpe: "str", wtool: "curl"})

                                }else{
                                    this.setState({tag: v, tpe: "cs", wtool:"telnet"})
                                }
                            }}
                        />
                        
                    </Form.Item>
                    <Form.Item>
                        <Select
                            style={{ width: '100%' }}
                            placeholder="选择诊断工具"
                            onChange={this.changeType}
                        >
                            {children}
                        </Select>
                        {
                            tpe == "str" ?
                                <Input onChange={e => this.setState({ inct: e.target.value })} placeholder="选择curl 时候不用填写，默认请求目标主机 80 端口 " />
                                :
                            tpe == "int" ?
                                <InputNumber style={{width:200}} placeholder="只填入数字" onChange={e => this.setState({ inct: e })} />
                                :
                            tpe == "cs"?
                                <Input onChange={e => this.setState({ inct: e.target.value })} placeholder="telnet 1.1.1.1 80  每一部分留空格" />
                                : null

                        }
                    </Form.Item>
                    <Form.Item>

                    <div style={{"display": this.state.loading}}><Icon   type="loading" />加载中</div>
                    <Button style={{ marginLeft: 20 }} type="default" icon="play-circle"
                        onClick={() => this.HandleSubmit()}     >提交检测</Button>
                    </Form.Item>

                    <Form.Item label="设置可访问的主机" style={{ padding: '0 20px' }}>
                        <Transfer
                            showSearch
                            listStyle={{ width: 740, maxHeight: 1600, minHeight: 300 }}
                            titles={['所有主机', '已选主机']}
                            dataSource={this.state.hosts}
                            targetKeys={store.hostPerms}
                            onChange={keys => store.hostPerms = keys}
                            filterOption={(inputValue, option) => `${option.top_project}${option.ipaddress}`.toLowerCase().indexOf(inputValue.toLowerCase()) > -1}
                            render={item => `${item.ipaddress} - ${item.top_project}`} />
                    </Form.Item>
                    <Form.Item label="诊断结果">
                        <TextArea value={resp} placeholder="" autoSize />
                    </Form.Item>
                    </div>
                )}
            </div>
        )
    }

}
export default NetTool
