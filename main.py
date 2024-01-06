import os
import shutil
import requests
from zipfile import ZipFile
from io import BytesIO
import subprocess

def download_and_extract_template(template_url, template_name):
    response = requests.get(template_url)

    if response.status_code == 200:
        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(template_name)
    else:
        print(f"Failed to download the template. Status code: {response.status_code}")
        exit(1)

def generate_android_files(package_name, app_name):
    # Create required directories
    os.makedirs(f'app/src/main/java/{package_name.replace(".", "/")}', exist_ok=True)
    os.makedirs('app/src/main/res/values', exist_ok=True)

    # Create or modify AndroidManifest.xml
    manifest_content = f"""
    <manifest xmlns:android="http://schemas.android.com/apk/res/android"
        package="{package_name}"
        android:versionCode="1"
        android:versionName="1.0">

        <application
            android:label="{app_name}"
            android:icon="@mipmap/ic_launcher">
            <!-- Add activities, services, etc. as needed -->
        </application>

    </manifest>
    """
    with open('app/src/main/AndroidManifest.xml', 'w') as manifest_file:
        manifest_file.write(manifest_content)

    # Create MainActivity.java
    main_activity_content = f"""
    package {package_name};

    import android.os.Bundle;
    import androidx.appcompat.app.AppCompatActivity;

    public class MainActivity extends AppCompatActivity {{
        @Override
        protected void onCreate(Bundle savedInstanceState) {{
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);
        }}
    }}
    """
    with open(f'app/src/main/java/{package_name.replace(".", "/")}/MainActivity.java', 'w') as main_activity_file:
        main_activity_file.write(main_activity_content)

    # Create strings.xml
    strings_content = f"""
    <resources>
        <string name="app_name">{app_name}</string>
    </resources>
    """
    with open('app/src/main/res/values/strings.xml', 'w') as strings_file:
        strings_file.write(strings_content)

def build_and_install():
    # Run Gradle build and install task
    subprocess.run(["./gradlew", "installDebug"])

def main():
    package_name = input("Enter package name (e.g., com.example.app): ")
    app_name = input("Enter app name: ")

    template_url = "https://github.com/hitherejoe/Android-Boilerplate/archive/master.zip"
    template_name = "android_template"

    # Download and extract the Android project template
    download_and_extract_template(template_url, template_name)

    # Generate Android files
    generate_android_files(package_name, app_name)

    # Navigate into the template directory
    template_directory = os.path.join(template_name, "Android-Boilerplate-master")
    os.chdir(template_directory)

    # Build and install the app
    build_and_install()

if __name__ == "__main__":
    main()
