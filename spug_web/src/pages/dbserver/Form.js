/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Input, Select, Col, Button, Upload, message,Icon,Checkbox,Radio} from 'antd';
import { http, X_TOKEN } from 'libs';
import store from './store';
import { Link } from 'react-router-dom';
import envStore from 'pages/config/environment/store';


@observer
class ComForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      uploading: false,
      password: null,
      addZone: null,
      fileList: [],
      editZone: store.record.zone,
      value: 4,
    }
  }

  componentDidMount() {
    if (store.record.pkey) {
      this.setState({
        fileList: [{uid: '0', name: '独立密钥', data: store.record.pkey}]
      })
    }

  }

  handleSubmit = () => {
    this.setState({loading: true});
    const formData = this.props.form.getFieldsValue();
    formData['id'] = store.record.id;
    const file = this.state.fileList[0];
    if (file && file.data) formData['pkey'] = file.data;
    console.log(formData)
    http.post('/api/host/resource/db/', formData)
      .then(res => {
          message.success('操作成功');
          store.formVisible = false;
          store.fetchRecords()
      }, () => this.setState({loading: false}))
  };

  handleConfirm = (formData) => {
    if (this.state.password) {
      formData['password'] = this.state.password;
      return http.post('/api/host/resource/db/', formData).then(res => {
        message.success('验证成功');
        store.formVisible = false;
        store.fetchRecords()
      })
    }
    message.error('请输入授权密码')
  };

  confirmForm = (username) => {
    return (
      <Form>
        <Form.Item required label="授权密码" help={`用户 ${username} 的密码， 该密码仅做首次验证使用，不会存储该密码。`}>
          <Input.Password onChange={val => this.setState({password: val.target.value})}/>
        </Form.Item>
      </Form>
    )
  };

  handleAddZone = () => {
    this.setState({zone: ''}, () => {
      Modal.confirm({
        icon: 'exclamation-circle',
        title: '添加主机类别',
        content: (
          <Form>
            <Form.Item required label="主机类别">
              <Input onChange={e => this.setState({addZone: e.target.value})}/>
            </Form.Item>
          </Form>
        ),
        onOk: () => {
          if (this.state.addZone) {
            store.zones.push(this.state.addZone);
            this.props.form.setFieldsValue({'zone': this.state.addZone})
          }
        },
      })
    });
  };

  handleEditZone = () => {
    this.setState({zone: store.record.zone}, () => {
      Modal.confirm({
        icon: 'exclamation-circle',
        title: '编辑主机类别',
        content: (
          <Form>
            <Form.Item required label="主机类别" help="该操作将批量更新所有属于该类别的主机并立即生效，如过只是想修改单个主机的类别请使用添加类别或下拉框选择切换类别。">
              <Input defaultValue={store.record.zone} onChange={e => this.setState({editZone: e.target.value})}/>
            </Form.Item>
          </Form>
        ),
        onOk: () => http.patch('/api/host/', {id: store.record.id, zone: this.state.editZone})
          .then(res => {
            message.success(`成功修改${res}条记录`);
            store.fetchRecords();
            this.props.form.setFieldsValue({'zone': this.state.editZone})
          })
      })
    });
  };

  handleUploadChange = (v) => {
    if (v.fileList.length === 0) {
      this.setState({fileList: []})
    }
  };

  handleUpload = (file, fileList) => {
    this.setState({uploading: true});
    const formData = new FormData();
    formData.append('file', file);
    http.post('/api/host/parse/', formData)
      .then(res => {
        file.data = res;
        this.setState({fileList: [file]})
      })
      .finally(() => this.setState({uploading: false}))
    return false
  };
  handleOsForm = (v) => {
    // console.log(v)
    //  1  win
    if(v==="Windows"){
      store.winformVisible = true;
      store.formVisible = false;
    }else {
      store.formVisible = true;
      store.winformVisible = false;
    }
  }

  render() {
    const info = store.record;
    const {fileList, loading, uploading} = this.state;
    const {getFieldDecorator} = this.props.form;
    return (
      <Modal
        visible
        width={800}
        maskClosable={false}
        title={store.record.id ? '编辑Linux类型数据库' : '新建Linux类型数据库'}
        okText="提交"
        onCancel={() => store.formVisible = false}
        confirmLoading={loading}
        onOk={this.handleSubmit}>
        <Form labelCol={{span: 5}} wrapperCol={{span: 17}}>
          {/* <Form.Item   style={{marginBottom: 0}}> */}
                {/* <Form.Item required label="系统类型" style={{ width: 'calc(30%)'}}>
                  {getFieldDecorator('ostp', {initialValue: info['ostp']})(
                    // <Input addonBefore="ssh" placeholder="用户名"/>
                    <Select  onChange={this.handleOsForm}  placeholder="系统类型">
                      <Select.Option value={"Linux"} key={0}>{"Linux"}</Select.Option>
                      <Select.Option value={"Windows"} key={1}>{"Windows"}</Select.Option>
                  </Select>
                  )}
                </Form.Item> */}
                {/* <Form.Item required label="资源类型"  style={{ width: 'calc(30%)'}}>
                  {getFieldDecorator('resource_type', {initialValue: info['resource_type']})(
                    // <Input addonBefore="ssh" placeholder="用户名"/>
                    <Select  placeholder="资源类型">
                      <Select.Option value={"主机"} key={0}>{"主机"}</Select.Option>
                      <Select.Option value={"数据库"} key={1}>{"数据库"}</Select.Option>
                      <Select.Option value={"redis"} key={2}>{"redis"}</Select.Option>
                  </Select>
                  )}
              </Form.Item> */}
            {/* </Form.Item> */}
          <Form.Item required label="系统类型" style={{marginBottom: 0}}>
                {getFieldDecorator('ostp', {initialValue: info['ostp']})(
                  // <Input addonBefore="ssh" placeholder="用户名"/>
                  <Select  onChange={this.handleOsForm}  placeholder="系统类型">
                    <Select.Option value={"Linux"} key={0}>{"Linux"}</Select.Option>
                    <Select.Option value={"Windows"} key={1}>{"Windows"}</Select.Option>
                </Select>
                )}
            </Form.Item>

          <Form.Item required label="资源类型" style={{marginBottom: 0}}>
          <Col span={17}>

                {getFieldDecorator('resource_type', {initialValue: info['resource_type']})(
                  // <Input addonBefore="ssh" placeholder="用户名"/>
                  <Select  placeholder="资源类型">
                    {/* <Select.Option value={"主机"} key={0}>{"主机"}</Select.Option> */}
                    {/* <Select.Option value={"数据库"} key={1}>{"数据库"}</Select.Option> */}
                    {/* <Select.Option value={"redis"} key={2}>{"redis"}</Select.Option> */}
                    {store.rset.map(item => (
                  // item.tag === "项目子类" ? 
                  // <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                  // : null
                      item.name === "数据库" ?
                      <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                      : null
                  ))}
                </Select>
                )}
                </Col>
                <Col span={5} offset={2}>
              <Link to="/config/resouret">新建资源类型</Link>
            </Col>
            </Form.Item>

          <Form.Item required label="实体项目">
            <Col span={19}>
            {getFieldDecorator('top_project', {initialValue: info['top_project']})(
                <Select  placeholder="实体项目"  mode="multiple">
                  {store.pj.map(item => (
                    item.tag === "实体项目" ? 
                    <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                    : null
                  ))}

                    {/* <Select.Option value={"东莞市政务数据大脑暨智慧城市IOC运行中心建设项目"} key={0}>{"东莞市政务数据大脑暨智慧城市IOC运行中心建设项目"}</Select.Option>
                    <Select.Option value={"东莞市疫情动态查询系统项目"} key={1}>{"东莞市疫情动态查询系统项目"}</Select.Option>
                    <Select.Option value={"东莞市疫情防控数据管理平台项目"} key={2}>{"东莞市疫情防控数据管理平台项目"}</Select.Option>
                    <Select.Option value={"东莞市跨境货车司机信息管理系统项目"} key={3}>{"东莞市跨境货车司机信息管理系统项目"}</Select.Option>
                    <Select.Option value={"疫情地图项目"} key={4}>{"疫情地图项目"}</Select.Option>
                    <Select.Option value={"粤康码"} key={5}>{"粤康码"}</Select.Option> */}
                </Select>
            )}
            </Col>
            <Col span={3} offset={2}>
              <Link to="/config/project">新建项目</Link>
            </Col>
          </Form.Item>
          <Form.Item required label="实体子项目">
          <Col span={17}>
              {getFieldDecorator('child_project',{initialValue: info['child_project']})(
                  <Select  placeholder="实体子项目"  mode="multiple">
                    {store.pj.map(item => (
                      item.tag === "项目子类" ? 
                      <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                      : null
                    ))}
                  </Select>
              )}
            </Col>
            <Col span={5} offset={2}>
              <Link to="/config/project">新建子项目</Link>
            </Col>
          </Form.Item>

          <Form.Item required label="资源类别">
          <Col span={16}>

            {/* <Col span={14}> */}
              {getFieldDecorator('zone', {initialValue: info['zone']})(
                <Select placeholder="资源类别"  mode="multiple" >
                  {store.zz.map(item => (
                  // item.tag === "项目子类" ? 
                  // <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                  // : null
                    (item.name).includes("数据库")?
                    <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                    : null
                  ))}
                </Select>
              )}
              </Col>
            {/* </Col> */}
            {/* <Col span={4} offset={1}>
              <Button type="link" onClick={this.handleAddZone}>添加类别</Button>
            </Col>
            <Col span={4} offset={1}>
              <Button type="link" onClick={this.handleEditZone}>编辑类别</Button>
            </Col> */}
            <Col span={6} offset={2}>
              <Link to="/config/zone">新建资源类别</Link>
            </Col>
          </Form.Item>
          <Form.Item required label="所属集群">
          <Col span={19}>

            {/* <Col span={14}> */}
              {getFieldDecorator('cluster', {initialValue: info['cluster']})(
                <Select placeholder="资源类别"  mode="multiple" >
                  {store.cs.map(item => (
                  // item.tag === "项目子类" ? 
                  // <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                  // : null
                    <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                  ))}
                </Select>
              )}
              </Col>
            {/* </Col> */}
            {/* <Col span={4} offset={1}>
              <Button type="link" onClick={this.handleAddZone}>添加类别</Button>
            </Col>
            <Col span={4} offset={1}>
              <Button type="link" onClick={this.handleEditZone}>编辑类别</Button>
            </Col> */}
              <Col span={3} offset={2}>
              <Link to="/config/cluster">新建集群</Link>
            </Col>
          </Form.Item>
          {/* <Form.Item required label="系统类型" style={{marginBottom: 0}}>
              <Form.Item style={{display: 'block', width: 'calc(30%)'}}>
                {getFieldDecorator('ostp', {initialValue: info['ostp']})(
                  // <Input addonBefore="ssh" placeholder="用户名"/>
                  <Select  onChange={this.handleOsForm}  placeholder="系统类型">
                    <Select.Option value={"Linux"} key={0}>{"Linux"}</Select.Option>
                    <Select.Option value={"Windows"} key={1}>{"Windows"}</Select.Option>
                </Select>
                )}
              </Form.Item>
            </Form.Item> */}
          {/* <Form.Item required label="主机名称">
            {getFieldDecorator('name', {initialValue: info['name']})(
              <Input placeholder="请输入主机名称"/>
            )}
          </Form.Item> */}
          <Form.Item required label="连接用户" style={{marginBottom: 0}}>
            <Form.Item style={{display: 'inline-block', width: 'calc(30%)'}}>
              {getFieldDecorator('username', {initialValue: info['username']})(
                // <Input addonBefore="ssh" placeholder="用户名"/>
                <Select  placeholder="用户">
                  {/* <Select.Option value={"root"} key={0}>{"root"}</Select.Option> */}
                  {/* <Select.Option value={"ioc"} key={1}>{"ioc"}</Select.Option> */}
                  {store.cuser.map(item => (
                  // item.tag === "项目子类" ? 
                  // <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                  // : null
                    <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                  ))}
              </Select>
              )}
            </Form.Item>
            <Form.Item style={{display: 'inline-block', width: 'calc(40%)'}}>
              {getFieldDecorator('ipaddress', {initialValue: info['ipaddress']})(
                <Input addonBefore="@" placeholder="IP" allowClear/>
              )}
            </Form.Item>
            <Form.Item style={{display: 'inline-block', width: 'calc(30%)'}}>
              {getFieldDecorator('port', {initialValue: info['port']})(
                <Input allowClear addonBefore="-p" placeholder="端口"/>
              )}
            </Form.Item>
          </Form.Item>
          <Form.Item required label="密码">
              {getFieldDecorator('password', {initialValue: info['password_hash'],rules: [{required: true, message: '请输入密码'}]})(
                <Input.Password
                  size="large"
                  type="password"
                  autoComplete="off"
                  placeholder="请输入密码"
                  allowClear
                  prefix={<Icon type="lock" />}/>
              )}
            </Form.Item>
            {/* <Form.Item required label="密码过期天数" >
                {getFieldDecorator('password_expire', {initialValue: info['password_expire'],rules: [{required: true, message: '密码过期天数'}]})(
                      <InputNumber />
                  )}
                
            </Form.Item> */}
{/* 
            <Form.Item required label="资源类型" style={{marginBottom: 0}}>
              <Form.Item style={{display: 'block', width: 'calc(30%)'}}>
                {getFieldDecorator('resource_type', {initialValue: info['resource_type']})(
                  // <Input addonBefore="ssh" placeholder="用户名"/>
                  <Select  placeholder="资源类型">
                    <Select.Option value={"主机"} key={0}>{"主机"}</Select.Option>
                    <Select.Option value={"数据库"} key={1}>{"数据库"}</Select.Option>
                    <Select.Option value={"redis"} key={2}>{"redis"}</Select.Option>
                </Select>
                )}
              </Form.Item>
            </Form.Item> */}
            <Form.Item required label="设备位置" style={{marginBottom: 0}}>
              <Col span={17}>

              {/* <Form.Item style={{display: 'block', width: 'calc(30%)'}}> */}
                {getFieldDecorator('provider', {initialValue: info['provider']})(
                  // <Input addonBefore="ssh" placeholder="用户名"/>
                  <Select  placeholder="设备位置">
                    {store.dvpo.map(item => (
                      <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                    ))}
                    {/* <Select.Option value={"电信"} key={0}>{"电信"}</Select.Option>
                    <Select.Option value={"联通"} key={1}>{"联通"}</Select.Option>
                    <Select.Option value={"移动"} key={2}>{"移动"}</Select.Option> */}
                </Select>
                )}
                </Col>
                <Col span={5} offset={2}>
                <Link to="/config/device">新建设备位置</Link>
              </Col>
              {/* </Form.Item> */}
            </Form.Item>
          
          {/* <Form.Item label="独立密钥" extra="默认使用全局密钥，如果上传了独立密钥则优先使用该密钥。">
            <Upload name="file" fileList={fileList} headers={{'X-Token': X_TOKEN}} beforeUpload={this.handleUpload}
                    onChange={this.handleUploadChange}>
              {fileList.length === 0 ? <Button loading={uploading} icon="upload">点击上传</Button> : null}
            </Upload>
          </Form.Item> */}
          {/* <Form.Item label="状态">
            {getFieldDecorator('status', {initialValue: info['status']})(
              <Input  placeholder="Y/N 上线或下线"/>
            )}
          </Form.Item> */}
          {/* <Form.Item required label="连接地址"  style={{display: 'inline-block', width: 'calc(30%)'}}>
              {getFieldDecorator('res_t', {initialValue: info['res_t']})(
                // <Input addonBefore="ssh" placeholder="用户名"/>
                <Select defaultValue={info["res_t"]}  placeholder="资源类型">
                  <Select.Option value={"host"} key={0}>{"主机"}</Select.Option>
                  <Select.Option value={"db"} key={1}>{"数据库"}</Select.Option>
                  <Select.Option value={"redis"} key={2}>{"redis"}</Select.Option>
              </Select>
              )}
            </Form.Item> */}

          <Form.Item  required label="业务IP">
            {getFieldDecorator('ipaddress', {initialValue: info['ipaddress']})(
              <Input  placeholder="内网ip地址"/>
            )}
          </Form.Item>
          {/* <Form.Item  label="服务包">
            <Col span={17}>

            {getFieldDecorator('service_pack', {initialValue: info['service_pack']})(
              // <Input  placeholder="服务包"/>
              <Select  placeholder="服务包"  mode="multiple">
                {store.svbag.map(item => (
                    <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                ))}
              </Select>
              
            )}
            </Col>
            <Col span={5} offset={2}>
                <Link to="/config/servicebag">新建服务包</Link>
              </Col>
          </Form.Item> */}
          <Form.Item  required label="所属区域">
          <Col span={17}>

            {getFieldDecorator('work_zone', {initialValue: info['work_zone']})(
              // <Input  placeholder="工作区域"/>
              <Select  placeholder="所属区域">
                {store.wz.map(item => (
                  <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                ))}
              </Select>
            )}
            </Col>
              <Col span={5} offset={2}>
                <Link to="/config/workzone">新建所属区域</Link>
              </Col>
          </Form.Item>
          <Form.Item   label="外网IP">
            {getFieldDecorator('outter_ip', {initialValue: info['outter_ip']})(
              <Input  placeholder="外网VIP"/>
            )}
          </Form.Item>
            <Form.Item   label="虚拟VIP">
            {getFieldDecorator('v_ip', {initialValue: info['v_ip']})(
              <Input  placeholder="虚拟VIP"/>
            )}
          </Form.Item>
          <Form.Item  required label="系统">
            {getFieldDecorator('osType', {initialValue: info['osType']})(
              <Input  placeholder="系统"/>
            )}
          </Form.Item>
          <Form.Item  required label="版本">
            {getFieldDecorator('osVerion', {initialValue: info['osVerion']})(
              <Input  placeholder="版本"/>
            )}
          </Form.Item>
          <Form.Item required label="环境">
            <Col span={17}>

              {getFieldDecorator('env_id', {initialValue: info['env_id']})(
                  <Select placeholder="环境">
                      {store.envs.map(item => (
                      <Select.Option value={item.id} key={item.id}>{item.name}</Select.Option>
                      ))}
                      {/* <Select.Option value={0} key={0}>{"生产"}</Select.Option>
                      <Select.Option value={1} key={1}>{"测试"}</Select.Option> */}
                  </Select>
              )}
              </Col>
              <Col span={5} offset={2}>
                  <Link to="/config/environment">新建环境</Link>
              </Col>
          </Form.Item>
          <Form.Item label="选择关系">
            {getFieldDecorator('dbrelation', {initialValue: info['dbrelation'] !=null ? info['dbrelation'] : 4})(
              <Radio.Group  >
                <Radio value={1}>主</Radio>
                <Radio value={2}>从</Radio>
                <Radio value={3}>集群</Radio>
                <Radio value={4}>无</Radio>
              </Radio.Group>
            )}
          </Form.Item>
          <Form.Item  label="实际用途">
            {getFieldDecorator('use_for', {initialValue: info['use_for']})(
              <Input.TextArea  placeholder="实际用途"/>
            )}
          </Form.Item>
          {/* <Form.Item  label="服务版本补丁">
            {getFieldDecorator('host_bug', {initialValue: info['host_bug']})(
              <Input.TextArea placeholder="host_bug"/>
            )}
          </Form.Item> */}
          {/* <Form.Item label="扩展配置">
            {getFieldDecorator('ext_config1', {initialValue: info['ext_config1']})(
              <Input placeholder="扩展配置"/>
            )}
          </Form.Item> */}
          <Form.Item label="开发负责人">
            {getFieldDecorator('developer', {initialValue: info['developer']})(
              <Input placeholder="developer"/>
            )}
          </Form.Item>
          <Form.Item label="运维负责人">
            {getFieldDecorator('opsper', {initialValue: info['opsper']})(
              <Input  placeholder="opsper"/>
            )}
          </Form.Item>
          {/* <Form.Item label="密钥">
            {getFieldDecorator('pkey', {initialValue: info['pkey']})(
                <Input.TextArea placeholder="密钥"/>
            )}
          </Form.Item> */}
          <Form.Item label="备注信息">
            {getFieldDecorator('comment', {initialValue: info['comment']})(
              <Input.TextArea placeholder="请输入主机备注信息"/>
            )}
          </Form.Item>
          {/* <Form.Item wrapperCol={{span: 14, offset: 6}}>
            <span role="img" aria-label="notice">⚠️ 首次验证时需要输入登录用户名对应的密码，但不会存储该密码。</span>
          </Form.Item> */}
        </Form>
      </Modal>
    )
  }
}

export default Form.create()(ComForm)
