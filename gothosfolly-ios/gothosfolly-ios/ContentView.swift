//
//  ContentView.swift
//  gothosfolly-ios
//
//  Created by Vishal Thapa on 19/06/22.
//

import SwiftUI

struct ContentView: View {
    
    @State var quote = [quotes]()
    var body: some View {
        Text("Hello, world!")
            .padding().onAppear(){
                Api().loadData{(quote) in self.quote = quote}
            }.navigationTitle("Quotes List")
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
