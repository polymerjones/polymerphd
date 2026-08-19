import SwiftUI

@main
struct PolymerPhDApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .ignoresSafeArea(.container, edges: .bottom)
                .preferredColorScheme(nil)   // follow the system; the page themes itself
        }
    }
}
