#!/usr/bin/env python3
"""Generate ios/PolymerPhD.xcodeproj/project.pbxproj.

The app is a WKWebView wrapper around app/index.html, which is copied into the
target's Resources. Keeping the project generated rather than checked in by hand
means it can be rebuilt after the web app changes, with stable object ids so the
file does not churn.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJ = ROOT / "ios" / "PolymerPhD.xcodeproj"

NAMES = ["prj","target","product","group_root","group_app","group_products","group_res",
         "f_app_swift","f_content_swift","f_assets","f_html","f_plist","f_product",
         "b_app_swift","b_content_swift","b_assets","b_html",
         "ph_sources","ph_frameworks","ph_resources",
         "cl_prj","cl_target","c_prj_debug","c_prj_release","c_tgt_debug","c_tgt_release"]
ID = {n: f"{i + 0x1000:024X}" for i, n in enumerate(NAMES)}

COMMON = """				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
				GCC_NO_COMMON_BLOCKS = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 17.0;
				SDKROOT = iphoneos;
				SWIFT_VERSION = 5.0;
"""

TARGET_COMMON = """				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = PolymerPhD/Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = "Polymer Ph.D.";
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.polymerphd.reference;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				TARGETED_DEVICE_FAMILY = "1,2";
"""

TEMPLATE = """// !$*UTF8*$!
{{
	archiveVersion = 1;
	classes = {{
	}};
	objectVersion = 56;
	objects = {{

/* Begin PBXBuildFile section */
		{b_app_swift} /* PolymerPhDApp.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {f_app_swift}; }};
		{b_content_swift} /* ContentView.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {f_content_swift}; }};
		{b_assets} /* Assets.xcassets in Resources */ = {{isa = PBXBuildFile; fileRef = {f_assets}; }};
		{b_html} /* index.html in Resources */ = {{isa = PBXBuildFile; fileRef = {f_html}; }};
/* End PBXBuildFile section */

/* Begin PBXFileReference section */
		{f_product} /* PolymerPhD.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = PolymerPhD.app; sourceTree = BUILT_PRODUCTS_DIR; }};
		{f_app_swift} /* PolymerPhDApp.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = PolymerPhDApp.swift; sourceTree = "<group>"; }};
		{f_content_swift} /* ContentView.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ContentView.swift; sourceTree = "<group>"; }};
		{f_assets} /* Assets.xcassets */ = {{isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = Assets.xcassets; sourceTree = "<group>"; }};
		{f_plist} /* Info.plist */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; }};
		{f_html} /* index.html */ = {{isa = PBXFileReference; lastKnownFileType = text.html; path = index.html; sourceTree = "<group>"; }};
/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
		{ph_frameworks} /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
		{group_root} = {{
			isa = PBXGroup;
			children = (
				{group_app} /* PolymerPhD */,
				{group_products} /* Products */,
			);
			sourceTree = "<group>";
		}};
		{group_app} /* PolymerPhD */ = {{
			isa = PBXGroup;
			children = (
				{f_app_swift} /* PolymerPhDApp.swift */,
				{f_content_swift} /* ContentView.swift */,
				{group_res} /* Resources */,
				{f_assets} /* Assets.xcassets */,
				{f_plist} /* Info.plist */,
			);
			path = PolymerPhD;
			sourceTree = "<group>";
		}};
		{group_res} /* Resources */ = {{
			isa = PBXGroup;
			children = (
				{f_html} /* index.html */,
			);
			path = Resources;
			sourceTree = "<group>";
		}};
		{group_products} /* Products */ = {{
			isa = PBXGroup;
			children = (
				{f_product} /* PolymerPhD.app */,
			);
			name = Products;
			sourceTree = "<group>";
		}};
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
		{target} /* PolymerPhD */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {cl_target};
			buildPhases = (
				{ph_sources} /* Sources */,
				{ph_frameworks} /* Frameworks */,
				{ph_resources} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = PolymerPhD;
			productName = PolymerPhD;
			productReference = {f_product} /* PolymerPhD.app */;
			productType = "com.apple.product-type.application";
		}};
/* End PBXNativeTarget section */

/* Begin PBXProject section */
		{prj} /* Project object */ = {{
			isa = PBXProject;
			attributes = {{
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1600;
				LastUpgradeCheck = 1600;
				TargetAttributes = {{
					{target} = {{
						CreatedOnToolsVersion = 16.0;
					}};
				}};
			}};
			buildConfigurationList = {cl_prj};
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = {group_root};
			productRefGroup = {group_products} /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				{target} /* PolymerPhD */,
			);
		}};
/* End PBXProject section */

/* Begin PBXResourcesBuildPhase section */
		{ph_resources} /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{b_html} /* index.html in Resources */,
				{b_assets} /* Assets.xcassets in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXResourcesBuildPhase section */

/* Begin PBXSourcesBuildPhase section */
		{ph_sources} /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{b_content_swift} /* ContentView.swift in Sources */,
				{b_app_swift} /* PolymerPhDApp.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXSourcesBuildPhase section */

/* Begin XCBuildConfiguration section */
		{c_prj_debug} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
{COMMON}				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_TESTABILITY = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				ONLY_ACTIVE_ARCH = YES;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = "DEBUG $(inherited)";
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			}};
			name = Debug;
		}};
		{c_prj_release} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
{COMMON}				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				SWIFT_COMPILATION_MODE = wholemodule;
				VALIDATE_PRODUCT = YES;
			}};
			name = Release;
		}};
		{c_tgt_debug} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
{TARGET_COMMON}			}};
			name = Debug;
		}};
		{c_tgt_release} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
{TARGET_COMMON}			}};
			name = Release;
		}};
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
		{cl_prj} /* Build configuration list for PBXProject "PolymerPhD" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{c_prj_debug} /* Debug */,
				{c_prj_release} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		{cl_target} /* Build configuration list for PBXNativeTarget "PolymerPhD" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{c_tgt_debug} /* Debug */,
				{c_tgt_release} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
/* End XCConfigurationList section */
	}};
	rootObject = {prj} /* Project object */;
}}
"""


def main():
    PROJ.mkdir(parents=True, exist_ok=True)
    (PROJ / "project.pbxproj").write_text(
        TEMPLATE.format(COMMON=COMMON, TARGET_COMMON=TARGET_COMMON, **ID), encoding="utf-8")

    # keep the bundled copy in step with the built web app
    src = ROOT / "app" / "index.html"
    dst = ROOT / "ios" / "PolymerPhD" / "Resources" / "index.html"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    print(f"Wrote {PROJ.relative_to(ROOT)}/project.pbxproj")
    print(f"Synced {dst.relative_to(ROOT)} ({dst.stat().st_size / 1_048_576:.2f} MB)")


if __name__ == "__main__":
    main()
