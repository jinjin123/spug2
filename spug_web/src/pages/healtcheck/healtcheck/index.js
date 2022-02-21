import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Table, message, Alert, Input, Select, Tabs, Button, Switch, Icon, Tag } from 'antd';
import { http, hasPermission } from 'libs';
import { SearchForm, AuthButton, AuthCard } from 'components';
import CmpFrom from './Form';

import store from './store';
const { TextArea } = Input;
const { Option } = Select;
const { Column } = Table;
const { TabPane } = Tabs;


@observer
class HealtCheck extends React.Component {
    constructor(props) {
        super(props);
        this.state = {

        }
    }
    componentDidMount() {
        store.fetchRecords();
    }
    onDelete = (info) => {
        Modal.confirm({
            title: '回收确认',
            content: `确定要回收【${info['url']}】?`,
            onOk: () => {
                return http.delete('/api/host/healtcheck/', { params: { id: info.id } })
                    .then(() => {
                        message.success('删除成功');
                        store.fetchRecords()
                    })
            }
        })
    }
    columns = [
        {
            title: '系统名称',
            dataIndex: 'name',
        },
        {
            title: '访问地址',
            dataIndex: 'url',
        },
        {
            title: '巡检时间',
            dataIndex: 'check_time',
        },
        {
            title: '巡检状态',
            dataIndex: 'status',
            render: status => {
                return <Tag color={status === 0 ? "green" : "volcano"} key={status}>
                    {status === 0 ? "正常" : "不正常"}
                </Tag>
            },
        },
        {
            title: '操作',
            render: info => {
                return <button onClick={this.onDelete.bind(this, info)}>删除</button>
            }
        },
    ]
    hostcolumns = [
        {
            title: 'ip',
            dataIndex: 'ipaddress',
            width: 120,
        },
        {
            title: 'cpu负载%',
            dataIndex: 'cpublance',
            width: 100,
        },
        {
            title: 'cpu逻辑核数',
            dataIndex: 'cpus',
            width: 100,
        },
        {
            title: '内存信息',
            dataIndex: 'meminfo',
        },
        {
            title: '内存负载%',
            dataIndex: 'memblance',
            width: 100,
        },
        {
            title: '磁盘信息',
            dataIndex: 'diskinfo',
            width: 600,
        },
        {
            title: '磁盘容量评估',
            dataIndex: 'diskstatus',
            width: 100,
            render: diskstatus => {
                return <Tag color={diskstatus === 0 ? "green" : diskstatus ===1 ?  "#f50" :  "volcano" } key={diskstatus}>
                {diskstatus === 0 ? "正常" : diskstatus ===1 ?  "准备爆满" : "还能用几天" }
            </Tag>
            }
            
        },
        {
            title: '状态评估',
            dataIndex: 'status',
            width: 100,
            render: status  => {
                return <Tag color={status === 0 ? "green" : status ===1 ?  "#f50" :  "volcano" } key={status}>
                {status === 0 ? "正常" : status ===1 ?  "需马上处理" : "还能缓几天处理" }
            </Tag>
            }
        },
        {
            title: '巡检时间',
            dataIndex: 'check_time',
        
        },

    ]
    render() {
        let data = store.records;
        let hostdata = store.hostdatas;

        return (
            <div>
                <Tabs >
                    <TabPane tab="系统访问巡检" key="1">
                        <AuthCard auth="deploy.rancher.view">
                            <SearchForm>
                                <SearchForm.Item span={4} style={{ textAlign: 'left' }}>
                                    <AuthButton auth="deploy.rancher.cmapdo"
                                        type="primary" icon="plus" onClick={() => store.showForm()}>添加系统访问检测</AuthButton>
                                </SearchForm.Item>
                            </SearchForm>
                        </AuthCard>
                        <Table
                            rowKey="id"
                            loading={store.isFetching}
                            dataSource={data}
                            columns={this.columns}

                            scroll={{ x: '100%' }}
                            pagination={{
                                showSizeChanger: true,
                                showLessItems: true,
                                hideOnSinglePage: true,
                                showTotal: total => `共 ${total} 条`,
                                pageSizeOptions: ['10', '20', '50', '100']
                            }}>


                        </Table>
                    </TabPane>
                    <TabPane tab="主机情况巡检（橘红色<85%<红色）" key="2">
                            <Table
                            rowKey="id"
                            loading={store.isFetching}
                            dataSource={hostdata}
                            columns={this.hostcolumns}

                            scroll={{ x: '100%' }}
                            pagination={{
                                showSizeChanger: true,
                                showLessItems: true,
                                hideOnSinglePage: true,
                                showTotal: total => `共 ${total} 条`,
                                pageSizeOptions: ['10', '20', '50', '100']
                            }}>


                        </Table>
                    </TabPane>
                    <TabPane tab="数据库情况巡检" key="3">
                    </TabPane>
                </Tabs>
                {store.formVisible && <CmpFrom />}
            </div>

        )
    }
}

export default HealtCheck