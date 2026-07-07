name: Build iOS IPA
on:
  workflow_dispatch:

jobs:
  build:
    runs-on: macos-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Xcode
        run: sudo xcode-select -s /Applications/Xcode.app

      - name: Build Archive
        run: |
          xcodebuild archive \
            -project PythonistaAppTemplate.xcodeproj \
            -scheme PythonistaAppTemplate \
            -configuration Release \
            -archivePath $GITHUB_WORKSPACE/build/App.xcarchive \
            CODE_SIGNING_ALLOWED=NO

      - name: Export IPA (Unsigned)
        run: |
          mkdir -p $GITHUB_WORKSPACE/Payload
          mv $GITHUB_WORKSPACE/build/App.xcarchive/Products/Applications/*.app $GITHUB_WORKSPACE/Payload/
          cd $GITHUB_WORKSPACE
          zip -r InstaDownloader.ipa Payload

      - name: Upload IPA Artifact
        uses: actions/upload-artifact@v4
        with:
          name: InstaDownloader-IPA
          path: ${{ github.workspace }}/InstaDownloader.ipa
