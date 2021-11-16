/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import {Modal, Form, Input, Checkbox,  Row, Col, message,Button,Radio,Select,Card,Icon} from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
// import historystore from '../rancherconfhisotry/store';
// import './form.css';
import { Action } from "components";
import  styles from "./index.module.css";
@observer
class DeployForm extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      loading: false,
        value: 1,
        input_value: 1,
        moreAction: [{"id":0,"v":"添加卷..."}]

    }
  }
  // componentDidMount() {
  //   historystore.fetchRecords();
  // }

  handleDelete = (text) => {
    Modal.confirm({
      title: '删除确认',
      content: `确定要删除【${text['name']}】?`,
      onOk: () => {
        return http.delete('/api/config/service/', {params: {id: text.id}})
          .then(() => {
            message.success('删除成功');
            store.fetchRecords()
          })
      }
    })
  };
  onChange = e => {
    console.log('radio checked', e.target.value);
    this.setState({
      value: e.target.value,
    });
  };

  handleSubmit = () => {
    this.setState({loading: true});
    const formData = this.props.form.getFieldsValue();
    console.log(formData,this.state.input_value,store.rancherport)
  };

  onVolumeChange = (action) => {
    switch(action){
      case "host":
        store.rancherVolume.push({"k":"映射主机目录" })
        this.setState({
          moreAction : [{"id": 1,"v":"映射主机目录"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "添加卷..."
          })
        },500)
        break;
      case "pvc":
        store.rancherVolume.push({"k":"使用现有的PVC" })
        this.setState({
          moreAction : [{"id": 2,"v":"使用现有的PVC"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "添加卷..."
          })
        },500)
        break;
      case "config":
        store.rancherVolume.push({"k":"配置映射卷"})
        this.setState({
          moreAction : [{"id": 3,"v":"配置映射卷"}]
        })
        setTimeout(() => {
          this.setState({
            moreAction : "添加卷..."
          })
        },500)
        break;
    }
  }
  

  onRadioInputChange = e => {
    this.setState({
      input_value: e.target.value,
    });
  };
  render() {
    // let data = store.vrecords;
    const {value} = this.state;
    const {input_value} = this.state;
    const { Option } = Select;
    const {getFieldDecorator} = this.props.form;

    // if (historystore.f_name) {
    //   data = data.filter(item => item['namespace'].toLowerCase().includes(historystore.f_name.toLowerCase()))
    // }
    return (
        <Modal
        visible
        width={1100}
        style={{ float: 'right',top: 0}}
        wrapClassName={'modalbox'}
        maskClosable={false}
        title={store.record.id ? '新应用服务部署' : '以现有应用服务部署'}
        onCancel={() => store.deployForm = false}
        onOk={this.handleSubmit}
        >
          <Form  layout="inline" wrapperCol={{ span: 24 }}>
              <Form.Item required label="名称"  rules={[{ required: true, message: '必填部署名' }]}>
                  {getFieldDecorator('task_name')(
                    <Input placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }}/>
                  )}
              </Form.Item>
              <Form.Item required label="工作负载类型"  rules={[{ required: true, message: '工作负载数量' }]}>
                  {getFieldDecorator('workloadnum')(
                    <Radio.Group onChange={this.onChange} >
                      <div className={styles.RadioVisbale}>
                          <Radio value={1}>Deployment: 部署无状态应用:<Input style={{ width: 50, marginLeft: 10 }} placeholder="" onChange={this.onRadioInputChange} />个 Pods</Radio>
                          <Radio value={2}>DaemonSet: 每台主机部署 {input_value} 个Pods</Radio>
                          <Radio value={3}>StatefulSet: 部署有状态应用 {input_value}个Pods </Radio>
                          <Radio value={4}>CronJob: 定时运行{input_value} 个Pods</Radio>
                          <Radio value={5}>Job: 一次性运行{input_value} 个Pods</Radio>
                        </div>
                    </Radio.Group>
                  )}
              </Form.Item>
          
                <Form.Item required label="Docker镜像" rules={[{ required: true, message: '必填镜像名' }]}>
                    {getFieldDecorator('image')(
                      <Input placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }}/>
                    )}
                </Form.Item>
                <Form.Item required label="命名空间" rules={[{ required: true, message: '必填命名空间' }]}>
                    {getFieldDecorator('namespace')(
                      <Input placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }}/>
                    )}
                </Form.Item>
              
                  <Form.Item  label="端口映射" >
                    {store.rancherport.map((item,index)=>(
                      <div key={index}>
                        <Col style={{ display:'flex'}}>
                          <Form.Item>
                                <Input placeholder="例如:tcp8080" defaultValue={item["portname"]}  onChange={e => item['portname'] = e.target.value} style={{ width: 150, marginLeft: 10 }}/>
                          </Form.Item>
                          <Form.Item>
                                <Input placeholder="容器端口" defaultValue={item["containerport"]} onChange={e => item['containerport'] = e.target.value}  style={{ width: 150, marginLeft: 10 }}/>
                          </Form.Item>
                          <Form.Item>
                                <Select defaultValue={item["potocol"]}  onChange={e => item['potocol'] = e.target.value} style={{ width: 100 }} >
                                  <Option value="TCP">TCP</Option>
                                  <Option value="UDP">UDP</Option>
                                </Select>
                          </Form.Item>
                          <Form.Item>
                                  <Select defaultValue={item["policy"]}  style={{ width: 280 }} >
                                    <Option value="NodePort">NodePort (所有主机端口均可访问)</Option>
                                    <Option value="HostPort">HostPort (仅 Pod 所在主机端口可访问)</Option>
                                    <Option value="ClusterIP">集群 IP(集群内部访问)</Option>
                                  </Select>
                          </Form.Item>
                          <Form.Item>
                                <Input value={item["targetport"]}  onChange={e => item['targetport'] = e.target.value} placeholder="默认NodePort随机端口30000-32768" style={{ width: 250, marginLeft: 10 }}/>
                          </Form.Item>
                            <div  onClick={() => store.rancherport.splice(index, 1)}>
                              <Icon type="minus-circle"/>移除
                            </div>
                          </Col>
                        </div>
                      ))}
                    <Button  type="dashed" block  
                      onClick={() => {store.rancherport.push({"portname":"","containerport":"","potocol":"","policy":"","targetport":""})}}>
                            <i type="plus">添加端口映射</i>
                    </Button>
                  </Form.Item>
                  <Form.Item label="环境变量" >
                    {store.rancherenv.map((item,index)=>(
                      <div key={index}>
                        <Col style={{ display:'flex'}}>
                          <Input   placeholder="键"  style={{ width: 300}}/> = <Input   placeholder="值" style={{ width: 300}}/>
                          <div  onClick={() => store.rancherenv.splice(index, 1)}>
                              <Icon type="minus-circle"/>移除
                          </div>
                        </Col>
                      </div>
                    ))}
                    <Button  type="dashed" block  
                      onClick={() => {store.rancherenv.push({"k":"","v":""})}}>
                            <i type="plus">添加环境变量</i>
                    </Button>
                  </Form.Item>

                  <Form.Item  label="主机调度" rules={[{ required: true, message: 'Please input your username!' }]}>
                      <Radio.Group  >
                        <Radio value={1}>指定主机运行所有 Pods
                            <Input placeholder="1.1.1.1" style={{ width: 200, marginLeft: 10 }}/>
                        </Radio>
                        <Radio value={2}>每个 Pod 自动匹配主机
                            <Card key="1" title="必须" style={{ width: 450 }}>
                                  <Input  placeholder="键" style={{ width: 150}}/>
                                  <Select defaultValue="="  style={{ width: 100 }} >
                                    <Option value="=">=</Option>
                                    <Option value="!=">≠</Option>
                                    <Option value="Exists">已设置</Option>
                                    <Option value="DoesNotExist">未设置</Option>
                                    <Option value="In">在列表中</Option>
                                    <Option value="NotIn">不在列表中</Option>
                                    <Option value="<">{"<"}</Option>
                                    <Option value=">">{">"}</Option>
                                  </Select>
                                  <Input  placeholder="值" style={{ width: 150}}/>
                            </Card>
                            <Card key="2" title="最好" style={{ width: 450 }}>
                                  <Input  placeholder="键" style={{ width: 150}}/>
                                  <Select defaultValue="="  style={{ width: 100 }} >
                                    <Option value="=">=</Option>
                                    <Option value="!=">≠</Option>
                                    <Option value="Exists">已设置</Option>
                                    <Option value="DoesNotExist">未设置</Option>
                                    <Option value="In">在列表中</Option>
                                    <Option value="NotIn">不在列表中</Option>
                                    <Option value="<">{"<"}</Option>
                                    <Option value=">">{">"}</Option>
                                  </Select>
                                  <Input  placeholder="值" style={{ width: 150}}/>
                            </Card>
                            <Card key="3" title="首选" style={{ width: 450 }}>
                                  <Input  placeholder="键" style={{ width: 150}}/>
                                  <Select defaultValue="="  style={{ width: 100 }} >
                                    <Option value="=">=</Option>
                                    <Option value="!=">≠</Option>
                                    <Option value="Exists">已设置</Option>
                                    <Option value="DoesNotExist">未设置</Option>
                                    <Option value="In">在列表中</Option>
                                    <Option value="NotIn">不在列表中</Option>
                                    <Option value="<">{"<"}</Option>
                                    <Option value=">">{">"}</Option>
                                  </Select>
                                  <Input  placeholder="值" style={{ width: 150}}/>
                            </Card>
                        </Radio>

                      </Radio.Group>
                  </Form.Item>

                  <Form.Item  label="数据卷" >
                        <Select value={this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "添加卷..."} style={{ width: 250 }} onChange={this.onVolumeChange.bind(this)} >
                          <Option value="pvc">使用现有PVC</Option>
                          <Option value="host">映射主机目录</Option>
                          <Option value="config">配置映射卷</Option>
                        </Select>
                        {store.rancherVolume.map((item,index)=>(
                          <div key={index} style={{ display:'flex'}}>
                            <Card title={item["k"]} style={{ width: 400 }}>
                                  <Input  placeholder="默认卷名vol2" value={"vol"+index} style={{ width: 350}}/>
                                  <Input  placeholder="默认权限模式" defaultValue="400" style={{ width: 350}}/>
                                  <Input   placeholder="容器路径" style={{ width: 350}}/>
                                  <Input   placeholder="子路径" style={{ width: 350}}/>
                                  
                            </Card>
                            <div  onClick={() => store.rancherVolume.splice(index, 1)}>
                              <Icon type="minus-circle"/>移除卷
                            </div>
                          </div>
                        ))}
                  </Form.Item>

              </Form>
        </Modal>
    )
  }
}
export default Form.create()(DeployForm)
