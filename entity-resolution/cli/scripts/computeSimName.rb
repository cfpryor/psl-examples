require 'set'

require 'jaro_winkler'

MIN_SIMILARITY = 0.75
SCALE = false

# Return: {name, ...}
def parseNames(authorNamesPath)
   names = Set.new()

   File.open(authorNamesPath, 'r'){|file|
      file.each{|line|
         parts = line.strip().split("\t")
         names << parts[1]
      }
   }

   return names
end

def cleanName(name)
   return name.downcase().gsub(/[^a-z]+/, ' ').strip().gsub(/\s+/, ' ')
end

# Return: [[name1, name2, sim], ...]
def computeSims(names)
   sims = []
   names = names.to_a()

   for i in 0...names.size() do
      for j in i...names.size() do
         name1 = names[i]
         name2 = names[j]

         if (i == j)
            sims << [name1, name2, 1.0]
            next
         end

         cleanName1 = cleanName(name1)
         cleanName2 = cleanName(name2)

         if (cleanName1 == cleanName2)
            sims << [name1, name2, 1.0]
            sims << [name2, name1, 1.0]
            next
         end

         # The library says "distance", but it is a similarity.
         sim = JaroWinkler.distance(cleanName1, cleanName2)

         if (sim < MIN_SIMILARITY)
            next
         end

         if (SCALE)
            sim = (sim - 0.75) * 4.0
         end

         sims << [name1, name2, sim]
         sims << [name2, name1, sim]
      end
   end

   return sims
end

def parseArgs(args)
   if (args.size != 1 || args.map{|arg| arg.gsub('-', '').downcase()}.include?('help'))
      puts "USAGE: ruby #{$0} <author names path>"
      exit(1)
   end

   path = args.shift()

   return [path]
end

def main(authorNamesPath)
   names = parseNames(authorNamesPath)
   sims = computeSims(names)

   # Sort for easier inspection.
   sims.sort!{|a, b| [a[0], -a[2], a[1]] <=> [b[0], -b[2], b[1]]}

   sims.each{|sim|
      puts sim.join("\t")
   }
end

if ($0 == __FILE__)
   main(*parseArgs(ARGV))
end
