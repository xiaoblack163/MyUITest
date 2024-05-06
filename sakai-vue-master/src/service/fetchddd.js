export function universalFetch(url, method = 'GET', data = null) {
  // 设置请求的选项
  const options = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // 如果提供了数据，则将其添加到请求体中
  if (data) {
    options.body = JSON.stringify(data);
  }

  // 使用fetch进行网络请求
  return fetch(url, options)
    .then(response => {
      // 如果响应状态码不是2xx，则抛出错误
      if (!response.ok) {
        throw new Error(`Network response was not ok ${response.statusText}`);
      }
      return response.json(); // 将响应数据解析为JSON
    })
    .catch(error => {
      // 处理请求过程中发生的错误
      console.error('There has been a problem with your fetch operation:', error);
      throw error; // 抛出错误，以供调用者处理
    });
}