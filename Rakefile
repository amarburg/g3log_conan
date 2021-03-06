
task :default => "debug:test"


@conan_opts = { shared: 'True', build_parallel: 'False' }
@conan_settings = {}
@conan_scopes = { build_tests: 'True' }
@conan_build = "missing"
load 'config.rb' if FileTest.readable? 'config.rb'

['Debug','Release'].each { |build_type|
  namespace build_type.downcase.to_sym do
    build_dir = ENV['BUILD_DIR'] || "build-#{build_type}"

    @conan_settings[:build_type] = build_type
    conan_opts = @conan_opts.each_pair.map { |key,val| "-o %s=%s" % [key,val] } +
                @conan_settings.each_pair.map { |key,val| "-s %s=%s" % [key,val] } +
                @conan_scopes.each_pair.map { |key,val| "--scope %s=%s" % [key,val] }

    task :build do
      FileUtils::mkdir build_dir unless FileTest::directory? build_dir
      sh "conan source ."
      chdir build_dir do
        sh "conan install %s .. --build=%s" % [conan_opts.join(' '), @conan_build]
        sh "conan build .."
      end
    end

    task :test => :build do
      #
    end
  end
}

namespace :conan do
  task :export do
    sh "rm -rf build-*"
    sh "conan export amarburg/testing"
  end

  task :upload do
    sh "conan upload g3log/master@amarburg/testing"
  end
end

namespace :dependencies do

  task :trusty do
    sh "sudo apt-get install -y cmake"
    sh "pip install conan"
  end

  task :osx do
    sh "brew update"
    # sh "brew tap homebrew/science"
    sh "pip install conan"
  end

  namespace :travis do
    task :linux => "dependencies:trusty"
    task :osx => "dependencies:osx"
   end

end
