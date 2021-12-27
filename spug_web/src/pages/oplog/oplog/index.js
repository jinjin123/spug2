import React from 'react';
import { observer } from 'mobx-react';
import { Input, Button, Select } from 'antd';
import { SearchForm, AuthDiv, AuthCard } from 'components';
import ComTable from './Table';

export default observer(function () {
    return (
        <AuthCard auth="oplog.oplog.view">
            <ComTable/>

        </AuthCard>
    )
})