/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Input,  message, Button } from 'antd';
import store from './store';
import './style.css';
import './html.css';
import './annotated.css';
@observer
class DiffForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      diffdata: null,
    }
  }

  // componentDidMount() {
  //   if (hostStore.records.length === 0) {
  //     hostStore.fetchRecords()
  //   }
  //   const file = lds.get(store, 'record.extra.1');
  //   if (file) {
  //     file.uid = '0';
  //     this.setState({fileList: [file]})
  //   }
  // }



  render() {

    const diffdata = store.delta
    const { TextArea } = Input;


    return (
      <Modal
        visible
        width={800}
        maskClosable={false}
        title="发布变更查看"
        onOk={() => store.diffVisble = false}
        onCancel={() => store.diffVisble = false}
        confirmLoading={this.state.loading}
        >
            <div id="visual"></div>

      </Modal>

    )
  }
}

export default Form.create()(DiffForm)
