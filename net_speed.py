import speedtest

st = speedtest.Speedtest()

st.get_best_server()
st.download()
st.upload()
st.results.share()

results_dict = st.results.dict()

download_speed = results_dict['download'] / (10**6)
upload_speed = results_dict['upload'] / (10**6)

print(f'下载速度: {download_speed} Mbps')
print(f'上传速度: {upload_speed} Mbps')
