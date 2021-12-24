/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Form, Input, Button, message, Divider, Alert, Icon, Select } from 'antd';
import Editor from 'react-ace';
import 'ace-builds/src-noconflict/mode-sh';
import 'ace-builds/src-noconflict/theme-tomorrow';
import styles from './index.module.css';
import { http, cleanCommand } from 'libs';
import store from './store';
import lds from 'lodash';
import 'codemirror/lib/codemirror.js';
import 'codemirror/lib/codemirror.css';
import 'codemirror/mode/yaml/yaml.js';
import 'codemirror/theme/monokai.css';
import 'codemirror/addon/scroll/annotatescrollbar.js'
import 'codemirror/addon/search/matchesonscrollbar.js'
import 'codemirror/addon/search/match-highlighter.js'
import 'codemirror/addon/search/jump-to-line.js'

import 'codemirror/addon/dialog/dialog.js'
import 'codemirror/addon/dialog/dialog.css'
import 'codemirror/addon/search/searchcursor.js'
import 'codemirror/addon/search/search.js'
// 折叠
import 'codemirror/addon/fold/foldcode.js';  // 代码折叠
import 'codemirror/addon/fold/foldgutter.js'; // 代码折叠
import 'codemirror/addon/fold/brace-fold.js'; // 代码折叠
import 'codemirror/addon/fold/comment-fold.js'; // 代码折叠
import 'codemirror/addon/lint/lint.js';  // 错误校验
import 'codemirror/addon/lint/javascript-lint.js';  // js错误校验
import 'codemirror/addon/lint/yaml-lint.js';
import 'codemirror/addon/selection/active-line.js';  // 当前行高亮
import 'codemirror/addon/lint/lint.css'  // 代码错误提示

import 'codemirror/addon/display/fullscreen.css';
import 'codemirror/addon/display/fullscreen.js';
import { Controlled as CodeMirror } from "react-codemirror2";
import { fullicon } from 'layout'
import styles2 from './form.module.css';
window.jsyaml = require('js-yaml')
@observer
class Ext2Setup3 extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      envs: this.isModify ? [store.record.env_id] : [],
      full: false,
      // configMap_v: [],
      fullmode:[],
      fullmode_flag: 0
    }
  }

  // componentDidMount() {
  //    console.log(store.record)
  // }

  handleFullmode = (index,status) => {
    //  console.log(index,status)
    store.showFullMode(index,status)
  }
  handleChange = (index,...value) => {
    store.record["configMap"][index]["v"] = value[3]
    // console.log(index,value)
    // this.setState({
    //   confingMap_v : this.state.configMap_v[index] = value[3]
    // })
  };
  handleSubmit = () => {
    this.setState({loading: true});
    // const info = store.deploy;
    // info['app_id'] = store.app_id;
    // info['extend'] = '2';
    // info['host_actions'] = info['host_actions'].filter(x => (x.title && x.data) || (x.title && (x.src || x.src_mode === '1') && x.dst));
    // info['server_actions'] = info['server_actions'].filter(x => x.title && x.data);
    store.record["pbtype"] = store.pbtype
    store.record["state"] = false
    store.record["desccomment"] = store.desccomment
    if (store.record['update_img'] === true && store.record['update_cmap'] === true){
      return message.error("必须更新镜像 或者是  配置映射卷")
    }
    http.post('/api/deploy/request/rancher/', store.record)
      .then( ()=> {
        message.success('建立发布审批单成功！');
        store.ext2Visible = false;
        store.addRancherVisible = false;
        store.page = 0;

      }, () => this.setState({loading: false}))
  };

  render() {
    const info = store.record;
    // console.log(info)
    const codeRead = store.codeRead;
    const { envs } = this.state;
    // const {fullmode,fullmode_flag} = this.state;
    // console.log(fullmode)、
    const fullmode = store.fullmode;
        // console.log(fullmode)
    // const configMap = store.configMap;
    const { value, onChange } = this.props;
    return (
      <Form labelCol={{span: 2}} wrapperCol={{span: 20}} className={styles.ext2Form}>
          <Alert
            closable
            showIcon
            type="info"
            message="小提示"
            style={{margin: '0 80px 20px'}}
            description={[
              <p key={1}>只更新镜像不需要修改配置则点击直接提交</p>,
              <p key={2}>配置映射配置已满足不需要继续添加Key value的话则直接点击提交 </p>,
              <p key={3}>如上面2点不满足则继续添加基于已关联的配置增量映射key value</p>,
            ]}/>
          {info["configMap"].map((item,index)=>(
            <div key={index}  style={{marginBottom: 30, position: 'relative'}} >
              <Form.Item required label={`Key${index+1}`} >
                  <Input value={item["k"]} onChange={e => item['k'] = e.target.value} placeholder="请输入" />
              </Form.Item>
              <Form.Item  required label="Value">
                  <Button size="small" className={styles2.fullscreen} onClick={this.handleFullmode.bind(this,index,true)}><img src={fullicon} /></Button>
                  {/* {this.props.form.getFieldDecorator('configMap_v', { initialValue: item['configMap_v'] })( */}
                  <CodeMirror
                    onBeforeChange={this.handleChange.bind(this,index,value)}
                    value={item["v"]}
                    options={{
                      mode: 'text/yaml',
                      theme: 'monokai',
                      smartIndent: true,
                      foldGutter: true,
                      lineWrapping: true,
                      gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter', 'CodeMirror-lint-markers'],
                      matchBrackets: true,
                      lineNumbers: true,
                      lint: true,
                      styleActiveLine: true,          // 选中行高亮
                      indentUnit: 4,
                      fullScreen: fullmode.length > 0 ? fullmode[index] : false,
                      readOnly: codeRead
                    }}
                  />
              </Form.Item>
              <div className={styles2.delAction} onClick={() => info["configMap"].splice(index, 1)}>
                <Icon type="minus-circle"/>移除
              </div>
            </div>
          ))}
        {!store.isReadOnly && (
          <Form.Item wrapperCol={{span: 14, offset: 6}}>
            <Button disabled={info["configName"] == "" ? true: false} type="dashed" block  onClick={() => {info["configMap"].push({"k":"","v":""});fullmode.push(false)}}>
                {info["configName"] == "" ? 
                    <i type="close">无配置文件映射卷</i>    : <i type="plus">添加key:value</i> }
            </Button>
          </Form.Item>
        )}
        <Form.Item wrapperCol={{span: 14, offset: 6}}>
          <Button
            type="primary"
            // disabled={store.isReadOnly || [...host_actions, ...server_actions].filter(x => x.title && x.data).length === 0}
            loading={this.state.loading}
            onClick={this.handleSubmit}>提交</Button>
          <Button style={{marginLeft: 20}} onClick={() => store.page -= 1}>上一步</Button>
        </Form.Item>
      </Form>
    )
  }
}

export default Ext2Setup3
