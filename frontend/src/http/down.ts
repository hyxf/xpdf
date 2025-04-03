import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

/**
 * 使用Axios发送POST请求（表单数据）并下载返回的文件流
 * @param api API端点URL
 * @param formData 要发送的表单数据对象
 * @param filename 可选的默认文件名，如果服务器没有提供Content-Disposition
 * @param token 可选的授权令牌
 * @returns Promise<void>
 */
export const downloadFileWithFormPost = async (
    api: string,
    formData: Record<string, string | number | boolean | File | Blob>,
    filename: string = 'output.pdf',
    token?: string
): Promise<void> => {
    try {
        // 创建FormData对象
        const form = new FormData();

        // 将表单数据添加到FormData对象
        Object.entries(formData).forEach(([key, value]) => {
            form.append(key, value.toString());
        });

        // 配置请求选项
        const config: AxiosRequestConfig = {
            method: 'post',
            url: api,
            data: form,
            responseType: 'blob',
            headers: {}
        };

        // 如果提供了令牌，添加到请求头
        if (token) {
            config.headers = {
                ...config.headers,
                'Authorization': `Bearer ${token}`
            };
        }

        // 发送请求
        const response: AxiosResponse<Blob> = await axios(config);

        // 获取blob数据
        const blob = new Blob([response.data]);

        // 尝试从响应头获取文件名
        const contentDisposition = response.headers['content-disposition'];
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
            if (filenameMatch && filenameMatch[1]) {
                filename = filenameMatch[1].replace(/['"]/g, '');
            }
        }

        // 创建一个临时的URL
        const url = window.URL.createObjectURL(blob);

        // 创建下载链接
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);

        // 触发下载
        link.click();

        // 清理
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error('下载文件时出错:', error instanceof Error ? error.message : String(error));
        throw error;
    }
};