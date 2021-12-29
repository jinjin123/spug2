/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Input, Checkbox, Row, Col, message, Button, Radio, Select, Card, Icon, Tag } from 'antd';
import { http, hasPermission } from 'libs';
import store from './store';
// import historystore from '../rancherconfhisotry/store';
// import './form.css';
import { Action } from "components";
import styles from "./index.module.css";
@observer
class DeployForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      value: 1,
      hostvalue: 2,
      input_value: 1,
      tmpns: [],
      tmpimg: [],
      tmppvc: [],
      tmpcmp: [],
      tmpimgs: {},
      choosens: {},
      tmpimgV: null,
      tmpnsV: null,
      vol: 0,
      cmapid: null,
      newNs: null,
      // rancherBL:{},
      moreAction: [{ "id": 0, "v": "添加卷..." }]

    }
  }
  // componentDidMount() {
  //   // historystore.fetchRecords();

  // }

  handleDelete = (text) => {
    Modal.confirm({
      title: '删除确认',
      content: `确定要删除【${text['name']}】?`,
      onOk: () => {
        return http.delete('/api/config/service/', { params: { id: text.id } })
          .then(() => {
            message.success('删除成功');
            store.fetchRecords()
          })
      }
    })
  };
  onChange = e => {
    this.setState({
      value: e.target.value,
    });
  };
  onCallHostChange = e => {
    // this.setState({
    //   hostvalue: e.target.value,
    // });
    if (e.target.value === 1) {
      store.rancherCallhost = []
      store.rancherCallhost.push({
        "type": "host", "itemid": 0, "itemdata": null,
      })
    } else {
      store.rancherCallhost = []
      store.rancherCallhost.push(
        { "type": "requireAll", "itemid": 1, "itemtitle": "必须", "itemdata": [{ "itemk": "", "itemtype": "=", "itemv": "" }] },
        { "type": "requireAny", "itemid": 2, "itemtitle": "最好", "itemdata": [{ "itemk": "", "itemtype": "=", "itemv": "" }] },
        { "type": "preferred", "itemid": 3, "itemtitle": "首选", "itemdata": [{ "itemk": "", "itemtype": "=", "itemv": "" }] }
      )
    }
  }
  onCallImgChange = e => {
    if (e.target.value === 1) {
      this.setState({
        tmpimgs: { "tag": "select" },
      });
    } else {
      this.setState({
        tmpimgs: { "tag": "input" },
      });
    }
  }
  onCallNsChange = e => {

    if (e.target.value === 1) {
      this.setState({
        choosens: { "tag": "select" },
      });
    } else {
      this.setState({
        choosens: { "tag": "input" },
      });
    }
  }
  onCallHostClick = e => {
    switch (e) {
      case 0:
        {
          store.rancherCallhost.map((item) => (
            item["itemid"] === 1 ? item["itemdata"].push({ "itemk": "", "itemtype": "=", "itemv": "" }) : null
          ))
        }
        break;;
      case 1:
        {
          store.rancherCallhost.map((item) => (
            item["itemid"] === 2 ? item["itemdata"].push({ "itemk": "", "itemtype": "=", "itemv": "" }) : null
          ))
        }
        break;;
      case 2:
        {
          store.rancherCallhost.map((item) => (
            item["itemid"] === 3 ? item["itemdata"].push({ "itemk": "", "itemtype": "=", "itemv": "" }) : null
          ))
        }
        break;;
    }
  }

  handleSubmit = () => {
    this.setState({ loading: true });
    const formData = this.props.form.getFieldsValue();
    const tmp = {}
    const requireAll = []
    const requireAny = []
    const preferred = []
    const node = {}
    const volumes = []
    const volumeMounts = []
    formData["scale"] = this.state.input_value
    formData["image"] = this.state.tmpimgV
    formData["namespaceId"] = this.state.tmpnsV
    formData["newNs"] = this.state.newNs


    formData["ports"] = store.rancherport
    if (this.state.cmapid != null) {
      formData["cmapid"] = formData['namespaceId'] + ":" + this.state.cmapid
    } else {
      formData["cmapid"] = null
    }
    formData["cname"] = this.state.cmapid

    store.rancherVolume.map(item => (
      item["tt"] === 0 ?
        (volumes.push({ "type": "volume", "name": item["vol"], "hostPath": { "type": "hostPathVolumeSource", "kind": null, "path": item["hostPath"] } }),
          volumeMounts.push({
            "readOnly": false,
            "type": "volumeMount",
            "mountPath": item["mountPath"],
            "name": item["vol"]
          }))
        : item["tt"] === 1 ?
          (volumes.push({
            "type": "volume", "name": item["vol"], "persistentVolumeClaim": {
              "readOnly": false,
              "type": "persistentVolumeClaimVolumeSource",
              "persistentVolumeClaimId": formData["namespaceId"] + ":" + item["pvc"]
            }
          }),
            volumeMounts.push({
              "readOnly": false,
              "type": "volumeMount",
              "mountPath": item["mountPath"],
              "subPath": item["subPath"],
              "name": item["vol"]
            }))
          : item["tt"] === 2 ?
            (volumes.push({
              "type": "volume", "name": item["vol"], "configMap": {
                "type": "configMapVolumeSource",
                "defaultMode": 256,
                "name": item["config"],
                "optional": false
              }
            }),
              volumeMounts.push({
                "readOnly": false,
                "type": "volumeMount",
                "mountPath": item["mountPath"],
                "subPath": item["subPath"],
                "name": item["vol"]
              }))
            : null
    ))
    formData["volumes"] = volumes
    formData["volumeMounts"] = volumeMounts


    store.rancherenv.map((item, index) => (
      // tmp['"' + item['k'] + '"']= item["v"]
      tmp[item['k']] = item["v"]

    ))
    formData["environment"] = tmp
    if (store.rancherCallhost.length > 2) {
      store.rancherCallhost.map((item, index) => (
        item['itemdata'].map((td) => (
          td['itemk'] != ""
            ?
            item["itemid"] === 1 ? requireAll.push(td["itemk"] + " " + td["itemtype"] + " " + td["itemv"]) :
              item["itemid"] === 2 ? requireAny.push(td["itemk"] + " " + td["itemtype"] + " " + td["itemv"]) :
                item["itemid"] === 3 ? preferred.push(td["itemk"] + " " + td["itemtype"] + " " + td["itemv"]) : null
            :
            null
        ))
      ))
    } else if (store.rancherCallhost.length === 1) {
      store.rancherCallhost.map(item => (
        node["nodeId"] = item["itemdata"]
      ))
    }
    if (requireAll.length > 0) {
      node["requireAll"] = requireAll
    }
    if (requireAny.length > 0) {
      node["requireAny"] = requireAny
    }
    if (preferred.length > 0) {
      node["preferred"] = preferred
    }
    formData["scheduling"] = { "node": node }
    http.post('/api/app/deploy/svcop/', { "data": formData, "env": 2, "tag": "ioc" })
      .then(() => {
        message.success('操作成功');
        store.deployForm = false;
        store.fetchRecords()

      }, () => this.setState({ loading: false }))
    // console.log(formData)
    store.rancherVolume = []
  };

  onVolumeChange = (action) => {
    let counter = this.state.vol
    console.log(counter)
    switch (action) {
      case "host":
        store.rancherVolume.push({ "t": "映射主机目录", "tt": 0, "tag": "host", "vol": "vol" + (counter).toString(), "mode": 256, "hostPath": "", "mountPath": "", "subPath": "" })
        this.setState({
          moreAction: [{ "id": 1, "v": "映射主机目录" }],
          vol: counter += 1
        })
        setTimeout(() => {
          this.setState({
            moreAction: "添加卷..."
          })
        }, 500)
        break;
      case "oldpvc":
        store.rancherVolume.push({ "t": "使用现有的PVC", "tt": 1, "tag": "oldpvc", "vol": "vol" + (counter).toString(), "mode": 256, "pvc": "", "mountPath": "", "subPath": "" })
        this.setState({
          moreAction: [{ "id": 2, "v": "使用现有的PVC" }]
        })
        setTimeout(() => {
          this.setState({
            moreAction: "添加卷...",
            vol: counter += 1
          })
        }, 500)
        break;
      case "newpvc":
        store.pvcForm = true;
        store.rancherVolume.push({ "t": "添加新的PVC" })
        this.setState({
          moreAction: [{ "id": 3, "v": "使用新的的PVC" }]
        })
        setTimeout(() => {
          this.setState({
            moreAction: "添加卷...",
            vol: counter += 1
          })
        }, 500)
        break;
      case "config":
        store.rancherVolume.push({ "t": "配置映射卷", "tt": 2, "tag": "config", "vol": "vol" + (counter).toString(), "mode": 256, "config": "", "mountPath": "", "subPath": "" })
        this.setState({
          moreAction: [{ "id": 4, "v": "配置映射卷" }]
        })
        setTimeout(() => {
          this.setState({
            moreAction: "添加卷...",
            vol: counter += 1
          })
        }, 500)
        break;
    }
  }

  onCallHostItemClick = (index, tindex) => {
    console.log(index, tindex)
    switch (tindex) {
      case 0:
        {
          store.rancherCallhost.map((item) => (
            item["itemid"] === 1 ? item["itemdata"].splice(index, 1) : null
          ))
        }
        break;;
      case 1:
        {
          store.rancherCallhost.map((item) => (
            item["itemid"] === 2 ? item["itemdata"].splice(index, 1) : null
          ))
        }
        break;;
      case 2:
        {
          store.rancherCallhost.map((item) => (
            item["itemid"] === 3 ? item["itemdata"].splice(index, 1) : null
          ))
        }
        break;;
    }
  }
  onRadioInputChange = e => {
    this.setState({
      input_value: e.target.value,
    });
  };
  onRjChange = v => {
    this.setState({
      tmpns: [],
      tmpimg: [],
      tmppvc: [],
      tmpcmp: []
    })
    let tmp = []
    let tmpimg = []
    let pvc = []
    let cmap = []
    let t = store.records.filter(item => item['pjname'] === v)
    t.map(item => {
      let newArr = store.pvcrecords.filter(x => x['nsname'] === item['nsname'])
      newArr.map(dd => {
        pvc.push(dd['pvcname'])
      })
      let newBrr = store.cmaprecords.filter(x => x['nsname'] === item['nsname'])
      newBrr.map(de => {
        cmap.push(de["configName"])
      })

    }
    )
    t.map(item => (
      tmp.push(item["nsname"]),
      tmpimg.push(item['img'])
    ))
    this.setState({
      tmpns: [... new Set(tmp)],
      tmpimg: [... new Set(tmpimg)],
      tmppvc: [... new Set(pvc)],
      tmpcmp: [... new Set(cmap)]
    })

  }

  render() {
    const clonedata = store.clonedeploy

    const { value,input_value } = this.state;
    const { Option } = Select;
    const { getFieldDecorator } = this.props.form;

    return (
      <Modal
        visible
        width={1100}
        style={{ float: 'right', top: 0 }}
        wrapClassName={'modalbox'}
        maskClosable={false}
        title={store.clonedeploy ? '克隆应用服务部署' : '以现有应用服务部署'}
        onCancel={() => (store.deployForm = false,store.clonedeploy=null)}
        onOk={this.handleSubmit}
      >
        {
          store.clonedeploy ?
            <Form layout="inline" wrapperCol={{ span: 24 }}>
              <Form.Item required label="名称" rules={[{ required: true, message: '必填部署名' }]}>
                {getFieldDecorator('name',{initialValue: clonedata.dpname})(
                  <Input   placeholder="统一" style={{ width: 410, marginLeft: 10 }} />
                )}
              </Form.Item>
              <Form.Item required label="工作负载类型" rules={[{ required: true, message: '工作负载数量' }]}>
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
              <Form.Item required label="rancher项目" rules={[{ required: true, message: '必填项目' }]}>
                {getFieldDecorator('pjname',{initialValue: clonedata.pjname})(
                  <Select onChange={v => this.onRjChange(v)} style={{ width: 200 }} >
                    {store.rancherpj.map((item, index) => (
                      <Option key={item} value={item}>{item}</Option>

                    ))}
                  </Select>
                )}
              </Form.Item>
              <Form.Item required label="命名空间" rules={[{ required: true, message: '必填命名空间' }]}>
                {getFieldDecorator('namespaceId')(
                  <Radio.Group  onChange={this.onCallNsChange} >
                    <Radio value={1}>使用现有：
                      {this.state.choosens["tag"] == "select"
                        ?
                        <Select
                          defaultValue={clonedata.nsname}
                          onChange={v => { this.setState({ tmpnsV: v, newNs: false }) }} style={{ width: 600 }}
                          style={{ width: 150 }} >
                          {this.state.tmpns.map((item, index) => (
                            <Option key={index} value={item}>{item}</Option>
                          ))}
                          <Option  key={100} value={clonedata.nsname}>{clonedata.nsname}</Option>
                        </Select>
                        : null
                      }
                    </Radio>
                    <Radio value={2}>创建命名空间：
                      {this.state.choosens["tag"] == "input"
                        ?
                        <Input defaultValue={clonedata.nsname} onChange={e => { this.setState({ tmpnsV: e.target.value, newNs: true }) }} placeholder="namespace" style={{ width: 150, marginLeft: 10 }} />
                        : null
                      }
                    </Radio>
                  </Radio.Group>
                )}
              </Form.Item>
              <Form.Item required label="Docker镜像" rules={[{ required: true, message: '必填镜像名' }]}>
                {getFieldDecorator('image')(
                  <Radio.Group onChange={this.onCallImgChange} >
                    <Radio value={1}>使用现有：
                      {this.state.tmpimgs["tag"] == "select"
                        ?
                        <Select
                          defaultValue={clonedata.img}
                          showSearch
                          filterOption={(input, option) =>
                            option.props.children.indexOf(input) >= 0
                          }
                          filterSort={(optionA, optionB) =>
                            optionA.props.children.localeCompare(optionB.props.children)
                          }
                          onChange={v => { this.setState({ tmpimgV: v }) }} style={{ width: 600 }} >
                          {this.state.tmpimg.map((item, index) => (
                            <Option key={item} value={item}>{item}</Option>
                          ))}
                        </Select>
                        : null
                      }
                    </Radio>
                    <Radio value={2}>更新镜像：
                      {this.state.tmpimgs["tag"] == "input"
                        ?
                        <Input defaultValue={clonedata.img} onChange={e => { this.setState({ tmpimgV: e.target.value }) }} placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }} />
                        : null
                      }
                    </Radio>
                  </Radio.Group>
                )}
              </Form.Item>
              <Form.Item label="端口映射" >
                
                {store.rancherport.length > 0 ? store.rancherport.map((item, index) => (
                  <div key={index}>
                    <Col style={{ display: 'flex' }}>
                      <Form.Item>
                        <Input placeholder="例如:tcp8080" defaultValue={item["name"]} onChange={e => item['name'] = e.target.value} style={{ width: 100, marginLeft: 5 }} />
                      </Form.Item>
                      <Form.Item>
                        <Input placeholder="容器端口" defaultValue={item["containerPort"]} onChange={e => item['containerPort'] = parseInt(e.target.value)} style={{ width: 100, marginLeft: 5 }} />
                      </Form.Item>
                      <Form.Item>
                        <Select defaultValue={item['protocol']} onChange={v => item['protocol'] = v} style={{ width: 100 }} >
                          <Option value="TCP">TCP</Option>
                          <Option value="UDP">UDP</Option>
                        </Select>
                      </Form.Item>
                      <Form.Item>
                        <Select defaultValue={"NodePort"} onChange={v => item['kind'] = v} style={{ width: 250 }} >
                          <Option value="NodePort">NodePort (所有主机端口均可访问)</Option>
                          <Option value="HostPort">HostPort (仅 Pod 所在主机端口可访问)</Option>
                          <Option value="ClusterIP">集群 IP(集群内部访问)</Option>
                        </Select>
                      </Form.Item>
                      <Form.Item>
                        <Input  defaultValue={item['sourcePort']} onChange={e => item['sourcePort'] = parseInt(e.target.value)} placeholder="随机30000-32768主机监听端口默认NodePort" style={{ width: 320, marginLeft: 5 }} />
                      </Form.Item>
                      <div onClick={() => store.rancherport.splice(index, 1)}>
                        <Icon type="minus-circle" />移除
                      </div>
                    </Col>
                  </div>
                )) : null}
                <Button type="dashed" block
                  onClick={() => { store.rancherport.push({ "name": "", "containerPort": null, "protocol": "TCP", "kind": "NodePort", "sourcePort": 0, "type": "containerPort", "hostPort": 0 }) }}>
                  <i type="plus">添加端口映射</i>
                </Button>
              </Form.Item>
              <Form.Item label="环境变量" >
                {store.rancherenv.length > 0 ? store.rancherenv.map((item, index) => (
                  <div key={index}>
                    <Col style={{ display: 'flex' }}>
                      <Input placeholder="键" defaultValue={item["k"]} onChange={e => item['k'] = e.target.value} style={{ marginRight: 10, width: 300 }} />
                      <Tag style={{ height: 32 }}>=</Tag>
                      <Input defaultValue={item["v"]} onChange={e => item['v'] = e.target.value} placeholder="值" style={{ width: 300 }} />
                      <div onClick={() => store.rancherenv.splice(index, 1)}>
                        <Icon type="minus-circle" />移除
                      </div>
                    </Col>
                  </div>
                )) : null}
                <Button type="dashed" block
                  onClick={() => { store.rancherenv.push({ "k": "", "v": "" }) }}>
                  <i type="plus">添加环境变量</i>
                </Button>
              </Form.Item>

              <Form.Item label="主机调度" rules={[{ required: true, message: '请选择调度方式!' }]}>
                <Radio.Group onChange={this.onCallHostChange} >
                  <Radio value={1}>指定主机运行所有 Pods
                    {store.rancherCallhost.length === 1
                      ?
                      <Select
                        showSearch
                        filterOption={(input, option) =>
                          option.props.children.indexOf(input) >= 0
                        }
                        filterSort={(optionA, optionB) =>
                          optionA.props.children.localeCompare(optionB.props.children)
                        }
                        onChange={v => store.rancherCallhost[0]["itemdata"] = v} style={{ width: 200, marginLeft: 10 }}>
                        {store.noderecords.map((t, tindex) => (
                          <Option key={tindex} value={t["nodeid"]}>{t["ipaddress"]}</Option>
                        ))
                        }
                      </Select>
                      : null}
                  </Radio>
                  <Radio value={2}>每个 Pod 自动匹配主机
                    {store.rancherCallhost.length > 1
                      ?
                      store.rancherCallhost.map((item, tindex) => (
                        <Card key={tindex} title={item["itemtitle"]} style={{ width: 450 }}>
                          {item["itemdata"].map((item, index) => (
                            <div key={index}>
                              <Input defaultValue={item["itemk"]} onChange={e => item['itemk'] = e.target.value} placeholder="键" style={{ width: 150 }} />
                              <Select defaultValue={item["itemtype"] != null ? item["itemtype"] : "="} onChange={v => item['itemtype'] = v} style={{ width: 100 }} >
                                <Option value="=">=</Option>
                                <Option value="!=">≠</Option>
                                <Option value="Exists">已设置</Option>
                                <Option value="DoesNotExist">未设置</Option>
                                <Option value="In">在列表中</Option>
                                <Option value="NotIn">不在列表中</Option>
                                <Option value="<">{"<"}</Option>
                                <Option value=">">{">"}</Option>
                              </Select>
                              <Input defaultValue={item["itemv"]} onChange={e => item['itemv'] = e.target.value} placeholder="值" style={{ width: 150 }} />
                              <div onClick={() => this.onCallHostItemClick(index, tindex)}>
                                <Icon type="minus-circle" />移除
                              </div>
                            </div>
                          ))}
                          <Button key={tindex} type="dashed" block onClick={() => this.onCallHostClick(tindex)}>
                            <i type="plus">添加规则</i>
                          </Button>
                        </Card>
                      ))
                      : null}
                  </Radio>
                </Radio.Group>
              </Form.Item>

              <Form.Item label="数据卷" >
                <Select value={this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "添加卷..."} style={{ width: 250 }} onChange={this.onVolumeChange.bind(this)} >
                  <Option value="oldpvc">使用现有PVC</Option>
                  <Option value="host">映射主机目录</Option>
                  <Option value="config">配置映射卷</Option>
                </Select>
                {store.rancherVolume.map((item, index) => (
                  <div key={index} style={{ display: 'flex' }}>
                    <Card title={item["t"]} style={{ width: 400 }}>
                      {item['tt'] === 0 ?
                        <div>
                          <Input onChange={e => item['vol'] = e.target.value} placeholder="默认卷名vol0" defaultValue={"vol" + index.toString()} value={"vol" + index.toString()} style={{ width: 350 }} />
                          <Input onChange={e => item['mode'] = e.target.value} placeholder="默认权限模式" defaultValue="256" style={{ width: 350 }} />
                          <Input onChange={e => item['hostPath'] = e.target.value} placeholder="主机路径" style={{ width: 350 }} />
                          <Input onChange={e => item['mountPath'] = e.target.value} placeholder="容器路径" style={{ width: 350 }} />
                          <Input onChange={e => item['subPath'] = e.target.value} placeholder="子路径" style={{ width: 350 }} />
                        </div>
                        : null}
                      {item['tt'] === 1 ?
                        <div>
                          <Input onChange={e => item['vol'] = e.target.value} placeholder="默认卷名vol1" defaultValue={"vol" + index.toString()} value={"vol" + index.toString()} style={{ width: 350 }} />
                          <Input onChange={e => item['mode'] = e.target.value} placeholder="默认权限模式" defaultValue="256" style={{ width: 350 }} />
                          <Select
                            showSearch
                            filterOption={(input, option) =>
                              option.props.children.indexOf(input) >= 0
                            }
                            filterSort={(optionA, optionB) =>
                              optionA.props.children.localeCompare(optionB.props.children)
                            }
                            onChange={v => item['pvc'] = v} >
                            {this.state.tmppvc.map((item, index) => (
                              <Option key={index} value={item}>{item}</Option>
                            ))}
                          </Select>
                          <Input onChange={e => item['mountPath'] = e.target.value} placeholder="容器路径" style={{ width: 350 }} />
                          <Input onChange={e => item['subPath'] = e.target.value} placeholder="子路径" style={{ width: 350 }} />
                        </div>
                        : null}
                      {item['tt'] === 2 ?
                        <div>
                          <Input onChange={e => item['vol'] = e.target.value} placeholder="默认卷名vol2" defaultValue={"vol" + index.toString()} value={"vol" + index.toString()} style={{ width: 350 }} />
                          <Input onChange={e => item['mode'] = e.target.value} placeholder="默认权限模式" defaultValue="256" style={{ width: 350 }} />
                          <Select
                            showSearch
                            filterOption={(input, option) =>
                              option.props.children.indexOf(input) >= 0
                            }
                            filterSort={(optionA, optionB) =>
                              optionA.props.children.localeCompare(optionB.props.children)
                            }
                            onChange={v => { item['config'] = v; this.setState({ "cmapid": v }) }} >
                            {this.state.tmpcmp.map(item => (
                              <Option key={item} value={item}>{item}</Option>
                            ))}
                          </Select>
                          <Input onChange={e => item['mountPath'] = e.target.value} placeholder="容器路径" style={{ width: 350 }} />
                          <Input onChange={e => item['subPath'] = e.target.value} placeholder="子路径" style={{ width: 350 }} />
                        </div>
                        : null}
                    </Card>
                    <div onClick={() => store.rancherVolume.splice(index, 1)}>
                      <Icon type="minus-circle" />移除卷
                    </div>
                  </div>
                ))}
              </Form.Item>
            </Form>
            : 
            <Form layout="inline" wrapperCol={{ span: 24 }}>
              <Form.Item required label="名称" rules={[{ required: true, message: '必填部署名' }]}>
                {getFieldDecorator('name')(
                  <Input placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }} />
                )}
              </Form.Item>
              <Form.Item required label="工作负载类型" rules={[{ required: true, message: '工作负载数量' }]}>
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
              <Form.Item required label="rancher项目" rules={[{ required: true, message: '必填项目' }]}>
                {getFieldDecorator('pjname')(
                  <Select onChange={v => this.onRjChange(v)} style={{ width: 200 }} >
                    {store.rancherpj.map((item, index) => (
                      <Option key={item} value={item}>{item}</Option>

                    ))}
                  </Select>
                )}
              </Form.Item>
              <Form.Item required label="命名空间" rules={[{ required: true, message: '必填命名空间' }]}>
                {getFieldDecorator('namespaceId')(
                  <Radio.Group onChange={this.onCallNsChange} >
                    <Radio value={1}>使用现有：
                      {this.state.choosens["tag"] == "select"
                        ?
                        <Select
                          onChange={v => { this.setState({ tmpnsV: v, newNs: false }) }} style={{ width: 600 }}
                          style={{ width: 150 }} >
                          {this.state.tmpns.map((item, index) => (
                            <Option key={index} value={item}>{item}</Option>
                          ))}
                        </Select>
                        : null
                      }
                    </Radio>
                    <Radio value={2}>创建命名空间：
                      {this.state.choosens["tag"] == "input"
                        ?
                        <Input onChange={e => { this.setState({ tmpnsV: e.target.value, newNs: true }) }} placeholder="namespace" style={{ width: 150, marginLeft: 10 }} />
                        : null
                      }
                    </Radio>
                  </Radio.Group>
                )}
              </Form.Item>
              <Form.Item required label="Docker镜像" rules={[{ required: true, message: '必填镜像名' }]}>
                {getFieldDecorator('image')(
                  <Radio.Group onChange={this.onCallImgChange} >
                    <Radio value={1}>使用现有：
                      {this.state.tmpimgs["tag"] == "select"
                        ?
                        <Select
                          showSearch
                          filterOption={(input, option) =>
                            option.props.children.indexOf(input) >= 0
                          }
                          filterSort={(optionA, optionB) =>
                            optionA.props.children.localeCompare(optionB.props.children)
                          }
                          onChange={v => { this.setState({ tmpimgV: v }) }} style={{ width: 600 }} >
                          {this.state.tmpimg.map((item, index) => (
                            <Option key={item} value={item}>{item}</Option>
                          ))}
                        </Select>
                        : null
                      }
                    </Radio>
                    <Radio value={2}>更新镜像：
                      {this.state.tmpimgs["tag"] == "input"
                        ?
                        <Input onChange={e => { this.setState({ tmpimgV: e.target.value }) }} placeholder="e.g. myapp" style={{ width: 410, marginLeft: 10 }} />
                        : null
                      }
                    </Radio>
                  </Radio.Group>
                )}
              </Form.Item>
              <Form.Item label="端口映射" >
                {store.rancherport.length > 0 ? store.rancherport.map((item, index) => (
                  <div key={index}>
                    <Col style={{ display: 'flex' }}>
                      <Form.Item>
                        <Input placeholder="例如:tcp8080" defaultValue={item["name"]} onChange={e => item['name'] = e.target.value} style={{ width: 100, marginLeft: 5 }} />
                      </Form.Item>
                      <Form.Item>
                        <Input placeholder="容器端口" defaultValue={item["containerPort"]} onChange={e => item['containerPort'] = parseInt(e.target.value)} style={{ width: 100, marginLeft: 5 }} />
                      </Form.Item>
                      <Form.Item>
                        <Select defaultValue={"TCP"} onChange={v => item['protocol'] = v} style={{ width: 100 }} >
                          <Option value="TCP">TCP</Option>
                          <Option value="UDP">UDP</Option>
                        </Select>
                      </Form.Item>
                      <Form.Item>
                        <Select defaultValue={"NodePort"} onChange={v => item['kind'] = v} style={{ width: 250 }} >
                          <Option value="NodePort">NodePort (所有主机端口均可访问)</Option>
                          <Option value="HostPort">HostPort (仅 Pod 所在主机端口可访问)</Option>
                          <Option value="ClusterIP">集群 IP(集群内部访问)</Option>
                        </Select>
                      </Form.Item>
                      <Form.Item>
                        <Input onChange={e => item['sourcePort'] = parseInt(e.target.value)} placeholder="随机30000-32768主机监听端口默认NodePort" style={{ width: 320, marginLeft: 5 }} />
                      </Form.Item>
                      <div onClick={() => store.rancherport.splice(index, 1)}>
                        <Icon type="minus-circle" />移除
                      </div>
                    </Col>
                  </div>
                )) : null}
                <Button type="dashed" block
                  onClick={() => { store.rancherport.push({ "name": "", "containerPort": null, "protocol": "TCP", "kind": "NodePort", "sourcePort": 0, "type": "containerPort", "hostPort": 0 }) }}>
                  <i type="plus">添加端口映射</i>
                </Button>
              </Form.Item>
              <Form.Item label="环境变量" >
                {store.rancherenv.length > 0 ? store.rancherenv.map((item, index) => (
                  <div key={index}>
                    <Col style={{ display: 'flex' }}>
                      <Input placeholder="键" defaultValue={item["k"]} onChange={e => item['k'] = e.target.value} style={{ marginRight: 10, width: 300 }} />
                      <Tag style={{ height: 32 }}>=</Tag>
                      <Input defaultValue={item["v"]} onChange={e => item['v'] = e.target.value} placeholder="值" style={{ width: 300 }} />
                      <div onClick={() => store.rancherenv.splice(index, 1)}>
                        <Icon type="minus-circle" />移除
                      </div>
                    </Col>
                  </div>
                )) : null}
                <Button type="dashed" block
                  onClick={() => { store.rancherenv.push({ "k": "", "v": "" }) }}>
                  <i type="plus">添加环境变量</i>
                </Button>
              </Form.Item>

              <Form.Item label="主机调度" rules={[{ required: true, message: '请选择调度方式!' }]}>
                <Radio.Group onChange={this.onCallHostChange} >
                  <Radio value={1}>指定主机运行所有 Pods
                    {store.rancherCallhost.length === 1
                      ?
                      <Select
                        showSearch
                        filterOption={(input, option) =>
                          option.props.children.indexOf(input) >= 0
                        }
                        filterSort={(optionA, optionB) =>
                          optionA.props.children.localeCompare(optionB.props.children)
                        }
                        onChange={v => store.rancherCallhost[0]["itemdata"] = v} style={{ width: 200, marginLeft: 10 }}>
                        {store.noderecords.map((t, tindex) => (
                          <Option key={tindex} value={t["nodeid"]}>{t["ipaddress"]}</Option>
                        ))
                        }
                      </Select>
                      : null}
                  </Radio>
                  <Radio value={2}>每个 Pod 自动匹配主机
                    {store.rancherCallhost.length > 1
                      ?
                      store.rancherCallhost.map((item, tindex) => (
                        <Card key={tindex} title={item["itemtitle"]} style={{ width: 450 }}>
                          {item["itemdata"].map((item, index) => (
                            <div key={index}>
                              <Input defaultValue={item["itemk"]} onChange={e => item['itemk'] = e.target.value} placeholder="键" style={{ width: 150 }} />
                              <Select defaultValue={item["itemtype"] != null ? item["itemtype"] : "="} onChange={v => item['itemtype'] = v} style={{ width: 100 }} >
                                <Option value="=">=</Option>
                                <Option value="!=">≠</Option>
                                <Option value="Exists">已设置</Option>
                                <Option value="DoesNotExist">未设置</Option>
                                <Option value="In">在列表中</Option>
                                <Option value="NotIn">不在列表中</Option>
                                <Option value="<">{"<"}</Option>
                                <Option value=">">{">"}</Option>
                              </Select>
                              <Input defaultValue={item["itemv"]} onChange={e => item['itemv'] = e.target.value} placeholder="值" style={{ width: 150 }} />
                              <div onClick={() => this.onCallHostItemClick(index, tindex)}>
                                <Icon type="minus-circle" />移除
                              </div>
                            </div>
                          ))}
                          <Button key={tindex} type="dashed" block onClick={() => this.onCallHostClick(tindex)}>
                            <i type="plus">添加规则</i>
                          </Button>
                        </Card>
                      ))
                      : null}
                  </Radio>
                </Radio.Group>
              </Form.Item>

              <Form.Item label="数据卷" >
                <Select value={this.state.moreAction[0]["id"] ? this.state.moreAction[0]["v"] : "添加卷..."} style={{ width: 250 }} onChange={this.onVolumeChange.bind(this)} >
                  <Option value="oldpvc">使用现有PVC</Option>
                  <Option value="host">映射主机目录</Option>
                  <Option value="config">配置映射卷</Option>
                </Select>
                {store.rancherVolume.map((item, index) => (
                  <div key={index} style={{ display: 'flex' }}>
                    <Card title={item["t"]} style={{ width: 400 }}>
                      {item['tt'] === 0 ?
                        <div>
                          <Input onChange={e => item['vol'] = e.target.value} placeholder="默认卷名vol0" defaultValue={"vol" + index.toString()} value={"vol" + index.toString()} style={{ width: 350 }} />
                          <Input onChange={e => item['mode'] = e.target.value} placeholder="默认权限模式" defaultValue="256" style={{ width: 350 }} />
                          <Input onChange={e => item['hostPath'] = e.target.value} placeholder="主机路径" style={{ width: 350 }} />
                          <Input onChange={e => item['mountPath'] = e.target.value} placeholder="容器路径" style={{ width: 350 }} />
                          <Input onChange={e => item['subPath'] = e.target.value} placeholder="子路径" style={{ width: 350 }} />
                        </div>
                        : null}
                      {item['tt'] === 1 ?
                        <div>
                          <Input onChange={e => item['vol'] = e.target.value} placeholder="默认卷名vol1" defaultValue={"vol" + index.toString()} value={"vol" + index.toString()} style={{ width: 350 }} />
                          <Input onChange={e => item['mode'] = e.target.value} placeholder="默认权限模式" defaultValue="256" style={{ width: 350 }} />
                          <Select
                            showSearch
                            filterOption={(input, option) =>
                              option.props.children.indexOf(input) >= 0
                            }
                            filterSort={(optionA, optionB) =>
                              optionA.props.children.localeCompare(optionB.props.children)
                            }
                            onChange={v => item['pvc'] = v} >
                            {this.state.tmppvc.map((item, index) => (
                              <Option key={index} value={item}>{item}</Option>
                            ))}
                          </Select>
                          <Input onChange={e => item['mountPath'] = e.target.value} placeholder="容器路径" style={{ width: 350 }} />
                          <Input onChange={e => item['subPath'] = e.target.value} placeholder="子路径" style={{ width: 350 }} />
                        </div>
                        : null}
                      {item['tt'] === 2 ?
                        <div>
                          <Input onChange={e => item['vol'] = e.target.value} placeholder="默认卷名vol2" defaultValue={"vol" + index.toString()} value={"vol" + index.toString()} style={{ width: 350 }} />
                          <Input onChange={e => item['mode'] = e.target.value} placeholder="默认权限模式" defaultValue="256" style={{ width: 350 }} />
                          <Select
                            showSearch
                            filterOption={(input, option) =>
                              option.props.children.indexOf(input) >= 0
                            }
                            filterSort={(optionA, optionB) =>
                              optionA.props.children.localeCompare(optionB.props.children)
                            }
                            onChange={v => { item['config'] = v; this.setState({ "cmapid": v }) }} >
                            {this.state.tmpcmp.map(item => (
                              <Option key={item} value={item}>{item}</Option>
                            ))}
                          </Select>
                          <Input onChange={e => item['mountPath'] = e.target.value} placeholder="容器路径" style={{ width: 350 }} />
                          <Input onChange={e => item['subPath'] = e.target.value} placeholder="子路径" style={{ width: 350 }} />
                        </div>
                        : null}
                    </Card>
                    <div onClick={() => store.rancherVolume.splice(index, 1)}>
                      <Icon type="minus-circle" />移除卷
                    </div>
                  </div>
                ))}
              </Form.Item>
            </Form>
        }
      </Modal>
    )
  }
}
export default Form.create()(DeployForm)
