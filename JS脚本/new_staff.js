async function RunPythonScript(rootRequest, pyName, parameter = {}, folderId = null) {
    if (!folderId) {
        let ret = await rootRequest.get(
            `/app-server/elements/get-element-info-by-name/base-info?elementName=${pyName}&elementType=PY`,
        ).then((res) => {
            return res
        });
        folderId = ret[0]['folderId']
    }
    const ret = await rootRequest.post(`/python-server2-0/start/python-web`, {
        data: {
            elementName: pyName,
            elementType: 'PY',
            // path: path,
            folderId: folderId,
            parameter: parameter,
        },
    }).then((res) => {
        return res
    });
    let result = ret
    return result
}
export default (params) => {
    const { formFn, rootRequest, globalInfo } = params;
    // 表单加载后运行
    const StaffInit = () => {
        setTimeout(() => {
            const emp_id = formFn.getFieldValue({ name: 'emp_id' });
            const emp_name = formFn.getFieldValue({ name: 'emp_name' });
            const email = formFn.getFieldValue({ name: 'email' });
            const dept_name = formFn.getFieldValue({ name: 'dept_name' });
            const emp_post = formFn.getFieldValue({ name: 'emp_post' });
            const emp_status = formFn.getFieldValue({ name: 'emp_status' });

            RunPythonScript(rootRequest, 'new_staff', {
                emp_id: emp_id?.value,
                emp_name: emp_name?.value,
                email: email?.value,
                dept_name: dept_name?.value,
                emp_post: emp_post?.value,
                emp_status: emp_status?.value,
            }).then((res) => {
                console.log("传参完成，就到这里吧！");
            })
        }, 0);
    };
    return {
        StaffInit,
    }

}