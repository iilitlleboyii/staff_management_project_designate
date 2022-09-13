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
    // 弹窗确认后运行
    const ProjectInit = () => {
        setTimeout(() => {
            const project_id = document.querySelector("input[data-name='project_id_add']");
            const project_name = document.querySelector("input[data-name='project_name_add']");
            // console.log(project_id);
            // console.log(project_name);

            RunPythonScript(rootRequest, 'add_project', {
                project_id: project_id?.value,
                project_name: project_name?.value,
            }).then((res) => {
                console.log("传参完成，就到这里吧！");
            })
        }, 0);
    };
    return {
        ProjectInit,
    }
}