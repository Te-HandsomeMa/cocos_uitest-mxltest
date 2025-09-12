from common.base_page import BasePage
from common.ws_server import rpc_server
import os

@rpc_server()
async def main(server):
    bp = BasePage(server=server,is_mobile_device=True,is_ios=False,device_id="172.16.36.4:5555")
    await bp.custom_command("setCamera Canvas/Camera")
    try:
        print("开始截图...")
        img = await bp.get_full_screen_shot()
        print(f"截图成功，图像尺寸: {img.shape}")
        
        print("保存截图...")
        bp.save_img(img, img_name="test.jpg")
        
        # 检查文件是否保存成功
        report_path = f"{bp.root_dir}/report"
        test_file_path = f"{report_path}/test.jpg"
        
        print(f"报告文件夹路径: {report_path}")
        print(f"测试文件路径: {test_file_path}")
        
        if os.path.exists(test_file_path):
            print("✅ 截图文件保存成功!")
            print(f"文件大小: {os.path.getsize(test_file_path)} bytes")
        else:
            print("❌ 截图文件保存失败!")
            
        # 列出report文件夹中的所有文件
        if os.path.exists(report_path):
            files = os.listdir(report_path)
            print(f"report文件夹中的文件: {files}")
        else:
            print("report文件夹不存在!")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bp.connect_close()

if __name__ == "__main__":
    main()
    





