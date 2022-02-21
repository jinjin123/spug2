import React from "react";
import { Controlled as CodeMirror } from "react-codemirror2";

class CodeMirrorWrapper extends React.Component {
    handleChange = (editor, data, value) => {
        this.props.onChange(value)
    };

    render() {
        // Antd's getFieldDecorator needs value & onChange
        // https://3x.ant.design/components/form-cn/#this.props.form.getFieldDecorator(id,-options)
        const { value, onChange, ...restProps } = this.props;
        return (
            <CodeMirror
                value={value}
                onBeforeChange={this.handleChange}
                {...restProps}
            />
        );
    }
}

export default CodeMirrorWrapper